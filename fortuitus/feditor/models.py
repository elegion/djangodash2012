from autoslug.fields import AutoSlugField
from django.db import models

from fortuitus.fcore.models import Company


class TestProject(models.Model):
    company = models.ForeignKey(Company)

    slug = AutoSlugField(populate_from='name')
    name = models.CharField(max_length=100)

    base_url = models.URLField()


class Params(models.Model):
    pass


class TestCase(models.Model):
    project = models.ForeignKey(TestProject)

    slug = AutoSlugField(populate_from='name')
    name = models.CharField(max_length=100)


class TestCaseStep(models.Model):
    pass




