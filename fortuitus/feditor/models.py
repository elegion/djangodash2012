from autoslug.fields import AutoSlugField
from django.db import models

from fortuitus.fcore.models import Company
from fortuitus.feditor.dbfields import ParamsField


class TestProject(models.Model):
    company = models.ForeignKey(Company)

    slug = AutoSlugField(populate_from='name')
    name = models.CharField(max_length=100)

    base_url = models.URLField()
    common_params = ParamsField()

    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.base_url)


class TestCase(models.Model):
    project = models.ForeignKey(TestProject)

    slug = AutoSlugField(populate_from='name')
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Method:
    GET = 'get'
    POST = 'post'

method_choices = (
    (Method.GET, 'get'),
    (Method.POST, 'post'),
)

class TestCaseStep(models.Model):
    testcase = models.ForeignKey(TestCase)
    order = models.PositiveSmallIntegerField()

    url = models.CharField(max_length=255)
    method = models.CharField(max_length=10, choices=method_choices, blank=True, null=True)
    params = ParamsField()

    def __unicode__(self):
        return self.url


class TestCaseAssert(models.Model):
    testcase = models.ForeignKey(TestCase)
    order = models.PositiveSmallIntegerField()

    expression = models.CharField(max_length=255)




