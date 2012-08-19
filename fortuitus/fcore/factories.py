from django.contrib.auth.models import User
import factory

from fortuitus.fcore import models


class UserF(factory.Factory):
    FACTORY_FOR = User


class CompanyF(factory.Factory):
    FACTORY_FOR = models.Company

    name = factory.Sequence(lambda n: 'Company #%s' % n)
