from autoslug.fields import AutoSlugField
from django.db import models

from fortuitus.feditor.dbfields import ParamsField


class Method:
    OPTIONS = 'OPTIONS'
    HEAD = 'HEAD'
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'
    PATCH = 'PATCH'


method_choices = [(f, f) for f in dir(Method) if not f.startswith('_')]


class TestProject(models.Model):
    """
    Test project.

    Contains info about API being tested and multiple test cases.

    """
    slug = AutoSlugField(populate_from='name')
    name = models.CharField(max_length=100)

    base_url = models.URLField()
    common_params = ParamsField(blank=True, null=True)

    class Meta:
        abstract = True


class Params(models.Model):
    """ HTTP request parameters for test cases. """
    pass

    class Meta:
        abstract = True


class TestCase(models.Model):
    """
    Test case.

    Contains multiple test case steps.

    Example test case could be:

     * Post tweet to Twitter.
     * Get user tweets.
     * Check last tweet is the one that was posted in step 1.

    """
    slug = AutoSlugField(populate_from='name')
    name = models.CharField(max_length=100)

    class Meta:
        abstract = True


class TestCaseStep(models.Model):
    """
    Test case step.

    Contains info about test requests and multiple assertions.
    """
    order = models.PositiveSmallIntegerField()

    url = models.CharField(max_length=255)
    method = models.CharField(max_length=10, choices=method_choices,
                              blank=True, null=True)
    params = ParamsField(blank=True, null=True)

    class Meta:
        abstract = True


class TestCaseAssert(models.Model):
    """
    Test case assertion.

    Contains assertions for a test case step.
    """
    order = models.PositiveSmallIntegerField()

    expression = models.CharField(max_length=255)

    class Meta:
        abstract = True
