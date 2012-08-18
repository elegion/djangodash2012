from django.test import TestCase
from django.utils import timezone
import mock

from core.tests import BaseTestCase
from fortuitus.feditor import factories as efactories, models as emodels
from fortuitus.frunner import factories as rfactories, models as rmodels
from fortuitus.frunner.tasks import run_tests


class TaskTestCase(BaseTestCase):
    def test_add(self):
        """
        Tests that 1 + 1 always equals 2. Asynchronously!
        """
        from fortuitus.frunner.tasks import add
        result = add.delay(1, 1)
        self.assertEqual(result.result, 2)


class RunTestsTaskTestCase(BaseTestCase):
    def test_non_existing_test(self):
        """ Should raise emodels.TestCase.DoesNotExist if test case not found
        """
        with self.assertRaises(emodels.TestCase.DoesNotExist):
            run_tests(10000)

    @mock.patch('fortuitus.frunner.models.TestCase.run', mock.Mock())
    def test_copies_and_runs_testcase(self):
        """
        Should copy TestCase (and all related models) int
        frunner.models.TestCase then perform frunner.models.TestCase.run()
        """
        test_case = efactories.TestCaseF.create()
        step1 = efactories.TestCaseStepF.create(testcase=test_case)
        step2 = efactories.TestCaseStepF.create(testcase=test_case)
        assertion_2_1 = efactories.TestCaseAssertF.create(step=step2)
        step3 = efactories.TestCaseStepF.create(testcase=test_case)
        assertion_3_1 = efactories.TestCaseAssertF.create(step=step3)
        assertion_3_2 = efactories.TestCaseAssertF.create(step=step3)

        run_tests(test_case.pk)

        rmodels.TestCase.run.assert_called_once_with()

        self.assertEqual(1, rmodels.TestCase.objects.count())
        test_case_copy = rmodels.TestCase.objects.all()[0]
        self.assertEqual(test_case.name, test_case_copy.name)
        self.assertEqual(test_case.slug, test_case_copy.slug)
        self.assertEqual(3, test_case_copy.steps.count())

        step1_copy = test_case_copy.steps.all()[0]
        self.assertEqual(step1.method, step1_copy.method)
        self.assertEqual(step1.order, step1_copy.order)
        self.assertEqual(step1.params, step1_copy.params)
        self.assertEqual(step1.url, step1_copy.url)
        self.assertEqual(0, step1_copy.assertions.count())

        step2_copy = test_case_copy.steps.all()[1]
        self.assertEqual(step2.method, step2_copy.method)
        self.assertEqual(step2.order, step2_copy.order)
        self.assertEqual(step2.params, step2_copy.params)
        self.assertEqual(step2.url, step2_copy.url)
        self.assertEqual(1, step2_copy.assertions.count())

        assertion_2_1_copy = step2_copy.assertions.all()[0]
        self.assertEqual(assertion_2_1.order, assertion_2_1_copy.order)
        self.assertEqual(assertion_2_1.lhs, assertion_2_1_copy.lhs)
        self.assertEqual(assertion_2_1.rhs, assertion_2_1_copy.rhs)
        self.assertEqual(assertion_2_1.operator, assertion_2_1_copy.operator)


class TestCaseModelTestCase(BaseTestCase):
    @mock.patch('fortuitus.frunner.models.TestCaseStep.run', mock.Mock(return_value=True))
    def test_run_runs_all_test_steps(self):
        """
        Test case should run all TestCaseSteps and mark self as success.
        """
        start = timezone.now()

        test_case = rfactories.TestCaseF.create()
        rfactories.TestCaseStepF.create(testcase=test_case)
        rfactories.TestCaseStepF.create(testcase=test_case)

        test_case.run()

        rmodels.TestCaseStep.run.assert_called_twice_with([])

        self.assertObjectUpdated(test_case,
            start_date__gte=start,
            end_date__gte=start,
            result=rmodels.TestResult.success)

    @mock.patch('fortuitus.frunner.models.TestCaseStep.run', mock.Mock(return_value=True))
    def test_run_without_test_steps(self):
        """
        Test case should be runnable without TestCaseSteps (and should be
        success).
        """
        start = timezone.now()
        test_case = rfactories.TestCaseF.create()

        test_case.run()

        self.assertEqual(0, rmodels.TestCaseStep.run.call_count)

        self.assertObjectUpdated(test_case,
                                 start_date__gte=start,
                                 end_date__gte=start,
                                 result=rmodels.TestResult.success)

    @mock.patch('fortuitus.frunner.models.TestCaseStep.run', mock.Mock(return_value=False))
    def test_marked_failed(self):
        """
        Test case should be marked as failed if TestCaseStep.run returns False.
        """
        start = timezone.now()
        test_case = rfactories.TestCaseF.create()
        rfactories.TestCaseStepF.create(testcase=test_case)
        rfactories.TestCaseStepF.create(testcase=test_case)

        test_case.run()

        self.assertEqual(1, rmodels.TestCaseStep.run.call_count)

        self.assertObjectUpdated(test_case,
                                 start_date__gte=start,
                                 end_date__gte=start,
                                 result=rmodels.TestResult.fail)

    def test_run_saves_exceptions(self):
        """
        Test case should save exceptions thrown by TestCaseStep.run
        (and mark self as error).
        """
        start = timezone.now()
        test_case = rfactories.TestCaseF.create()
        rfactories.TestCaseStepF.create(testcase=test_case)
        rfactories.TestCaseStepF.create(testcase=test_case)

        def raise_exception(*args, **kwargs):
            raise Exception('asdf')

        with mock.patch('fortuitus.frunner.models.TestCaseStep.run', raise_exception):
            test_case.run()

        self.assertObjectUpdated(test_case,
                                 start_date__gte=start,
                                 end_date__gte=start,
                                 result=rmodels.TestResult.error)


class TestCaseAssertTestCase(TestCase):
    def test_do_assertion(self):
        responses = [{'status_code': '404'}, {'status_code': '200'}]
        a = rmodels.TestCaseAssert()

        a.lhs = '0.status_code'
        a.operator = 'Eq'
        a.rhs = '404'
        self.assertTrue(a.do_assertion(responses))

        a.lhs = '.status_code'
        a.operator = 'Eq'
        a.rhs = '404'
        self.assertFalse(a.do_assertion(responses))


class ResolversTestCase(TestCase):
    def test_resolve_operator_short_name(self):
        """ Tests operator resolver with short operator name. """
        from . import resolvers, operators
        Op = resolvers.resolve_operator('Eq')
        self.assertEqual(Op, operators.Eq)

    def test_resolve_operator_full_name(self):
        """
        Tests operator resolver with full operator name, including module.
        """
        from . import resolvers, operators
        Op = resolvers.resolve_operator('fortuitus.frunner.operators.Eq')
        self.assertEqual(Op, operators.Eq)

    def test_resolve_lhs_last_response(self):
        """ Test lhs resolver: last response, dictionary. """
        from .resolvers import resolve_lhs
        responses = [{'status_code': 404}, {'status_code': 200}]
        self.assertEqual(resolve_lhs('.status_code', responses), 200)

    def test_resolve_lhs_arbitrary_response(self):
        """ Test lhs resolver: arbitrary response, dictionary. """
        from .resolvers import resolve_lhs
        responses = [{'status_code': 404}, {'status_code': 200}]
        self.assertEqual(resolve_lhs('0.status_code', responses), 404)

    def test_resolve_lhs_object(self):
        """ Test lhs resolver: arbitrary response, object. """
        from .resolvers import resolve_lhs
        responses = [type('TestResp', (), {'status_code': 200})]
        self.assertEqual(responses[0].status_code, 200)
        self.assertEqual(resolve_lhs('0.status_code', responses), 200)

    def test_resolve_rhs_plain_value(self):
        """ Test rhs resolver: plain value. """
        from .resolvers import resolve_rhs
        self.assertEqual(resolve_rhs(1, []), 1)
        self.assertEqual(resolve_rhs('foo', []), 'foo')

    def test_resolve_rhs_reference(self):
        """ Test rhs resolver: step reference. """
        from .resolvers import resolve_rhs
        responses = [{'status_code': 404}, {'status_code': 200}]
        self.assertEqual(resolve_rhs('1.status_code', responses), 200)


class OperatorsTestCase(TestCase):
    def test_Eq(self):
        from .operators import Eq
        eq = Eq(1, 1)
        self.assertTrue(eq.run())
        eq = Eq(1, 2)
        self.assertFalse(eq.run())
