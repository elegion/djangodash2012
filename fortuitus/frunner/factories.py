import factory
from fortuitus.feditor.factories import TestProjectF

from fortuitus.frunner import models


class TestCaseF(factory.Factory):
    FACTORY_FOR = models.TestCase

    project = factory.SubFactory(TestProjectF)
    name = factory.Sequence(lambda n: 'TestCase #%s' % n)


class TestCaseStepF(factory.Factory):
    FACTORY_FOR = models.TestCaseStep

    testcase = factory.SubFactory(TestCaseF)
    order = 1
    method = models.models_base.Method.GET
    url = 'user_list.json'


class TestCaseAssertF(factory.Factory):
    FACTORY_FOR = models.TestCaseAssert

    step = factory.SubFactory(TestCaseStepF)
    order = 1
    lhs = ''
    rhs = ''
    operator = models.models_base.method_choices[0][0]
