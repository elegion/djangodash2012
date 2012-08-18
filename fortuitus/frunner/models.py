from django.db import models
from django.utils import timezone
from jsonfield import JSONField
import requests

from fortuitus.feditor import models_base
from fortuitus.feditor.models import TestProject
from fortuitus.frunner.resolvers import (resolve_lhs, resolve_rhs,
                                         resolve_operator)


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


class TestCase(models_base.TestCase):
    """
    Contains information about actual test case run.

    See also :model:`feditor.TestCase`
    """
    project = models.ForeignKey(TestProject, related_name='test_runs')

    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    result = models.CharField(max_length=10, choices=TEST_CASE_RESULT_CHOICES,
                              blank=False, null=True)

    def run(self):
        self.start_date = timezone.now()

        responses = []
        for step in self.steps.all():
            try:
                if not step.run(responses):
                    break
            except:
                self.result = TestResult.error
                break
        else:
            self.result = TestResult.success

        self.result = self.result or TestResult.fail
        self.end_date = timezone.now()
        self.save()


class Params(models_base.Params):
    """ HTTP request parameters for test cases. """
    pass


class TestCaseStep(models_base.TestCaseStep):
    """
    Contains information about test step run result.

    See also :model:`feditor.TestCaseStep`
    """
    testcase = models.ForeignKey(TestCase, related_name='steps')

    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    result = models.CharField(max_length=10, choices=TEST_CASE_RESULT_CHOICES,
                              blank=False, null=True)

    response_code = models.PositiveSmallIntegerField(null=True, blank=True)
    response_headers = JSONField(null=True, blank=True)
    response_body = models.TextField(null=True, blank=True)

    def run(self, responses):
        r = requests.request(self.method, self.url)

        self.response_code = r.status_code
        self.response_body = r.text
        self.response_headers = r.headers
        responses.push(r)

        for assertion in self.assertions:
            assertion.do_assertion(responses)


class TestCaseAssert(models_base.TestCaseAssert):
    """
    Contains assertion result for TestCaseStep

    See also :model:`feditor.TestCaseAssert`
    """
    step = models.ForeignKey(TestCaseStep, related_name='assertions')

    result = models.CharField(max_length=10, choices=TEST_CASE_RESULT_CHOICES,
                              blank=False, null=True)

    def do_assertion(self, responses):
        lhs = resolve_lhs(self.lhs, responses)
        rhs = resolve_rhs(self.rhs, responses)
        operator = resolve_operator(self.operator)(lhs, rhs)
        return operator.run()
