import factory
from fortuitus.fcore.factories import CompanyF

from fortuitus.feditor import models


class TestProjectF(factory.Factory):
    FACTORY_FOR = models.TestProject

    company = factory.SubFactory(CompanyF)
    name = factory.Sequence(lambda n: 'TestProject #%s' % n)

    base_url = 'http://api.example.com/'


class TestCaseF(factory.Factory):
    FACTORY_FOR = models.TestCase

    project = factory.SubFactory(TestProjectF)
    name = factory.Sequence(lambda n: 'TestCase #%s' % n)


class TestCaseStepF(factory.Factory):
    FACTORY_FOR = models.TestCaseStep

    order = 1
    method = models.models_base.Method.GET
    url = 'user_list.json'

class TestCaseAssertF(factory.Factory):
    FACTORY_FOR = models.TestCaseAssert

    order = 1
    lhs = ''
    rhs = ''
    operator = models.models_base.method_choices[0][0]
