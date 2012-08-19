import logging

from django.db import models
from django.forms.models import model_to_dict
from django.utils import timezone
from furl import furl
from jsonfield import JSONField
from oauth_hook import OAuthHook
import requests

from fortuitus.feditor import models_base
from fortuitus.feditor.dbfields import ParamsField
from fortuitus.feditor.models import TestProject
from fortuitus.frunner.resolvers import (resolve_lhs, resolve_rhs,
                                         resolve_operator)

logger = logging.getLogger(__name__)


class TestResult:
    pending = 'pending'
    success = 'success'
    fail = 'fail'
    error = 'error'


TEST_CASE_RESULT_CHOICES = (
    (TestResult.success, 'success'),
    (TestResult.fail, 'fail'),
    (TestResult.error, 'error'),
)


class TestRun(models.Model):
    """ Contains information about single project tests run. """
    project = models.ForeignKey(TestProject, related_name='test_runs')

    base_url = models.URLField()
    common_params = ParamsField(blank=True, null=True)

    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    result = models.CharField(max_length=10, choices=TEST_CASE_RESULT_CHOICES,
                              blank=False, null=True)

    def __unicode__(self):
        return u'%s (%s)' % (self.project.name, self.base_url)

    def result_str(self):
        return self.result or TestResult.pending

    def human_name(self):
        return 'Run #%s (%s)' % (self.pk, self.result or TestResult.pending)

    @property
    def number(self):
        return self.pk

    @staticmethod
    def create_from_project(project):
        testrun = TestRun.objects.create(project=project,
                                         base_url=project.base_url,
                                         common_params=project.common_params)
        # Now copy all testcases and related data
        for etest in project.testcases.all():
            kwargs = model_to_dict(etest, exclude=['id', 'project'])
            rtest = TestCase.objects.create(testrun=testrun, **kwargs)

            for estep in etest.steps.all():
                kwargs = model_to_dict(estep, exclude=['id', 'testcase'])
                rstep = TestCaseStep.objects.create(testcase=rtest, **kwargs)

                for assertion in estep.assertions.all():
                    kwargs = model_to_dict(assertion, exclude=['id', 'step'])
                    TestCaseAssert.objects.create(step=rstep, **kwargs)
        return testrun

    def run(self):
        logger.info('Starting TestRun %s', self)
        self.start_date = timezone.now()
        self.save()

        for testcase in self.testcases.all():
            testcase.run(self)
            if testcase.result != TestResult.success:
                self.result = TestResult.fail

        self.end_date = timezone.now()
        self.result = self.result or TestResult.success
        self.save()
        logger.info('Finished TestRun %s (result=%s)', self, self.result)
        return self.result

    def failed_tests(self):
        return self.testcases.filter(result=TestResult.fail)

    def error_tests(self):
        return self.testcases.filter(result=TestResult.error)

    def passed_tests(self):
        return self.testcases.filter(result=TestResult.success)


class TestCase(models_base.TestCase):
    """
    Contains information about actual test case run.

    See also :model:`feditor.TestCase`.
    """
    testrun = models.ForeignKey(TestRun, related_name='testcases')

    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    result = models.CharField(max_length=10, choices=TEST_CASE_RESULT_CHOICES,
                              blank=False, null=True)
    exception = models.TextField(blank=True, null=True)

    def result_str(self):
        return self.result or TestResult.pending

    def run(self, testrun):
        """ Runs the test case attached to :param testrun:. """
        logger.info('Starting TestCase %s', self)
        self.start_date = timezone.now()
        try:
            session = self.handle_auth()
        except Exception as e:
            self.result = TestResult.error
            self.exception = '%s: %s' % (e.__class__.__name__, str(e))
        else:
            self.run_steps(testrun, self.steps.all(), session)
        self.result = self.result or TestResult.fail
        self.end_date = timezone.now()
        self.save()

    def handle_auth(self):
        """ Handles test authentication. """
        login = self.login_options
        if self.login_type == models_base.LoginType.NONE:
            session = requests.session()
        elif self.login_type == models_base.LoginType.BASIC:
            session = requests.session(auth=(login['user'], login['password']))
        elif self.login_type == models_base.LoginType.COOKIE:
            session = requests.session()
            params = {login['login_field']: login['login'],
                      login['password_field']: login['password']}
            session.post(self.login_info['url'], params=params)
        elif self.login_type == models_base.LoginType.OAUTH:
            params = dict(access_token=login['access_token'],
                          access_token_secret=login['access_token_secret'],
                          consumer_key=login['consumer_key'],
                          consumer_secret=login['consumer_secret'],
                          header_auth=login.get('header_auth', True))
            oauth_hook = OAuthHook(**params)
            session = requests.session(hooks={'pre_request': oauth_hook})
            logger.info('Attaching OAuth info.')
        else:
            raise NotImplementedError('%s login type not implemented' %
                                      self.login_type)
        return session

    def run_steps(self, testrun, steps, session):
        """ Runs test case steps. """
        responses = []
        for step in steps:
            try:
                response = step.run(testrun, self, session, responses)
                if response is False:
                    logger.warn('TestCase %s received False response', self)
                    break
            except Exception, e:
                logger.error('TestCase %s exception: %s', self, e)
                logger.error(e)
                self.exception = unicode(e)
                self.result = TestResult.error
                break
        else:
            self.result = TestResult.success

        self.result = self.result or TestResult.fail
        self.end_date = timezone.now()
        self.save()
        logger.info('Finished TestCase %s (result=%s)', self, self.result)


class TestCaseStep(models_base.TestCaseStep):
    """
    Contains information about test step run result.

    See also :model:`feditor.TestCaseStep`.
    """
    testcase = models.ForeignKey(TestCase, related_name='steps')

    resolved_params = ParamsField(blank=True, null=True)

    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    result = models.CharField(max_length=10, choices=TEST_CASE_RESULT_CHOICES,
                              blank=False, null=True)
    exception = models.TextField(blank=True, null=True)


    response_code = models.PositiveSmallIntegerField(null=True, blank=True)
    response_headers = JSONField(null=True, blank=True)
    response_body = models.TextField(null=True, blank=True)

    def result_str(self):
        return self.result or TestResult.pending

    def get_params(self):
        """ Returns [(resolved_param.name, param.value, resolved_param.value)]
        """
        if self.resolved_params:
            for name, value in self.resolved_params.iteritems():
                yield name, self.params[name], value

    def get_response_code_name(self):
        from requests.status_codes import _codes
        try:
            return _codes[self.response_code][0].upper().replace('_', ' ')
        except IndexError:
            return 'UNKNOWN'

    def run(self, testrun, testcase, session, responses):
        """ Runs test case step. """
        logger.info('Starting TestStep %s', self)
        self.start_date = timezone.now()
        self.resolved_params = self.params.resolve()
        self.save()

        try:
            url = furl(testrun.base_url)
            url.join(self.url)
            logger.info('Senging request: %s %s', self.method, url.url)
            if self.method in (models_base.Method.POST, models_base.Method.PUT, models_base.Method.PATCH):
                data = self.resolved_params
                params = {}
            else:
                data = {}
                params = self.resolved_params
            r = session.request(self.method, url.url, data=data, params=params)

            logger.info('Received response: %s (headers: %s)', r.status_code, r.headers)
            logger.debug('Response body: %s', r.text)
            self.response_code = r.status_code
            self.response_body = r.text
            self.response_headers = r.headers

            for assertion in self.assertions.all():
                assertion.do_assertion(responses + [r])

            logger.info('Finished TestStep %s (result=%s)', self, TestResult.success)
            return r
        except Exception, e:
            logger.error('Exception during TestStep %s: %s', self, e)
            logger.error(e)
            self.exception = '%s: %s' % (e.__class__.__name__, str(e))
            if isinstance(e, AssertionError):
                self.result = TestResult.fail
                return False
            else:
                self.result = TestResult.error
                raise
        finally:
            self.end_date = timezone.now()
            self.result = self.result or TestResult.success
            self.save()


class TestCaseAssert(models_base.TestCaseAssert):
    """
    Contains assertion result for TestCaseStep.

    See also :model:`feditor.TestCaseAssert`.
    """
    step = models.ForeignKey(TestCaseStep, related_name='assertions')

    lhs_value = models.CharField(max_length=256, default='')
    rhs_value = models.CharField(max_length=256, default='')
    result = models.CharField(max_length=10, choices=TEST_CASE_RESULT_CHOICES,
                              blank=False, null=True)

    def result_str(self):
        return self.result or TestResult.pending

    def do_assertion(self, responses):
        logger.info('Performing assertion: %s', self)
        self.lhs_value = unicode(resolve_lhs(self.lhs, responses))
        self.rhs_value = unicode(resolve_rhs(self.rhs, responses))
        operator = resolve_operator(self.operator)
        if not operator(self.lhs_value, self.rhs_value):
            logger.warn('Assertion failed: %s %s %s', self.lhs_value, self.operator, self.rhs_value)
            self.result = TestResult.fail
            self.save()
            raise AssertionError('%s should be %s %s'
                                 % (self.lhs_value, self.operator, self.rhs_value))
        self.result = TestResult.success
        self.save()
        logger.info('Assertion OK: %s %s %s', self.lhs, self.operator, self.rhs)
        return True
