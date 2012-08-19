from autoslug.fields import AutoSlugField
from django.db import models

from fortuitus.fcore.models import Company
from fortuitus.feditor import models_base
from fortuitus.feditor.dbfields import ParamsField


class TestProjectManager(models.Manager):
    def get_by_company(self, company):
        return TestProject.objects.filter(company=company)


class TestProject(models.Model):
    """
    Test project.

    Contains info about API being tested and multiple test cases.

    """
    company = models.ForeignKey(Company)
    slug = AutoSlugField(populate_from='name')
    name = models.CharField(max_length=100)

    base_url = models.URLField()
    common_params = ParamsField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    objects = TestProjectManager()

    class Meta():
        ordering = ('slug',)

    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.base_url)


class TestCaseManager(models.Manager):
    new_name = 'New Test'

    def get_unique_new_name(self):
        """
        Generates unique test case name.

        FIXME: thread unsafe, ugly method.
        """
        names = self.filter(name__istartswith=self.new_name) \
                .values_list('name', flat=True)
        idx = 1
        while '%s %d' % (self.new_name, idx) in names:
            idx += 1
        return '%s %d' % (self.new_name, idx)


class TestCase(models_base.TestCase):
    """
    Test case.

    Contains multiple test case steps.

    Example test case could be:

     * Post tweet to Twitter.
     * Get user tweets.
     * Check last tweet is the one that was posted in step 1.

    """
    project = models.ForeignKey(TestProject, related_name='testcases')

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    objects = TestCaseManager()

    class Meta():
        ordering = ('created',)


class TestCaseStep(models_base.TestCaseStep):
    """
    Test case step.

    Contains info about test requests and multiple assertions.
    """
    testcase = models.ForeignKey(TestCase, related_name='steps')

    class Meta():
        ordering = ('order',)


class TestCaseAssert(models_base.TestCaseAssert):
    """
    Test case assertion.

    Contains assertions for a test case step.
    """
    step = models.ForeignKey(TestCaseStep, related_name='assertions')
