from django.db import models
from jsonfield import JSONField
import requests

from fortuitus.feditor import models_base


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
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    result = models.CharField(max_length=10, choices=TEST_CASE_RESULT_CHOICES, blank=False, null=True)

    def run(self):
        responses = []
        for step in self.steps:
            step.run(responses)


class Params(models_base.Params):
    """ HTTP request parameters for test cases. """
    pass


class TestCaseStep(models_base.TestCaseStep):
    """
    Contains information about test step run result.

    See also :model:`feditor.TestCaseStep`
    """
    testcase = models.ForeignKey(TestCase, related_name='steps')

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    result = models.CharField(max_length=10, choices=TEST_CASE_RESULT_CHOICES, blank=False, null=True)

    response_code = models.PositiveSmallIntegerField()
    response_headers = JSONField()
    response_body = models.TextField()

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

    result = models.CharField(max_length=10, choices=TEST_CASE_RESULT_CHOICES, blank=False, null=True)

    def do_assertion(self, responses):
        pass
