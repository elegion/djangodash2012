from django.db import models

from fortuitus.fcore.models import Company
from fortuitus.feditor import models_base


class TestProject(models_base.TestProject):
    """
    Test project.

    Contains info about API being tested and multiple test cases.

    """
    company = models.ForeignKey(Company)

    slug = AutoSlugField(populate_from='name')
    name = models.CharField(max_length=100)

    base_url = models.URLField()
    common_params = ParamsField(blank=True, null=True)

    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.base_url)


class Params(models_base.Params):
    """ HTTP request parameters for test cases. """
    pass


class TestCase(models_base.TestCase):
    """
    Test case.

    Contains multiple test case steps.

    Example test case could be:

     * Post tweet to Twitter.
     * Get user tweets.
     * Check last tweet is the one that was posted in step 1.

    """
    project = models.ForeignKey(TestProject)

    def __unicode__(self):
        return self.name


class TestCaseStep(models_base.TestCaseStep):
    """
    Test case step.

    Contains info about test requests and multiple assertions.
    """
    testcase = models.ForeignKey(TestCase)
    order = models.PositiveSmallIntegerField()

    url = models.CharField(max_length=255)
    method = models.CharField(max_length=10, choices=method_choices,
                              blank=True, null=True)
    params = ParamsField(blank=True, null=True)

    def __unicode__(self):
        return self.url


class TestCaseAssert(models_base.TestCaseAssert):
    """
    Test case assertion.

    Contains assertions for a test case step.
    """
    step = models.ForeignKey(TestCaseStep)
