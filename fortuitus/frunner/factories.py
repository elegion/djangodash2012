import factory
from fortuitus.feditor.factories import TestProjectF
from fortuitus.feditor.params import Params

from fortuitus.frunner import models


class TestRunF(factory.Factory):
    FACTORY_FOR = models.TestRun

    project = factory.SubFactory(TestProjectF)
    base_url = 'http://api.example.com/'


class TestCaseF(factory.Factory):
    FACTORY_FOR = models.TestCase

    testrun = factory.SubFactory(TestRunF)
    name = factory.Sequence(lambda n: 'TestCase #%s' % n)
    order = 1
    login_type = models.models_base.LoginType.NONE


class TestCaseStepF(factory.Factory):
    FACTORY_FOR = models.TestCaseStep

    testcase = factory.SubFactory(TestCaseF)
    order = 1
    method = models.models_base.Method.GET
    url = 'user_list.json'

    @classmethod
    def _prepare(cls, create, **kwargs):
        kwargs['params'] = Params(**kwargs.get('params', {}))
        return super(TestCaseStepF, cls)._prepare(create, **kwargs)


class TestCaseAssertF(factory.Factory):
    FACTORY_FOR = models.TestCaseAssert

    step = factory.SubFactory(TestCaseStepF)
    order = 1
    lhs = ''
    rhs = ''
    operator = models.models_base.method_choices[0][0]
