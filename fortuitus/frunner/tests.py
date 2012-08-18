from django.test import TestCase
import mock
from fortuitus.feditor import models as emodels
from fortuitus.frunner import factories, models as rmodels
from fortuitus.frunner.tasks import run_tests


class TaskTestCase(TestCase):
    def test_add(self):
        """
        Tests that 1 + 1 always equals 2. Asynchronously!
        """
        from fortuitus.frunner.tasks import add
        result = add.delay(1, 1)
        self.assertEqual(result.result, 2)


class RunTestsTaskTestCase(TestCase):
    def test_non_existing_test(self):
        with self.assertRaises(emodels.TestCase.DoesNotExist):
            run_tests(10000)

    @mock.patch('fortuitus.frunner.models.TestCase.run', mock.Mock())
    def test_copies_and_runs_testcase(self):
        test_case = factories.TestCaseF.create()
        step1 = factories.TestCaseStepF.create(testcase=test_case)
        step2 = factories.TestCaseStepF.create(testcase=test_case)
        assertion_2_1 = factories.TestCaseAssertF.create(step=step2)
        step3 = factories.TestCaseStepF.create(testcase=test_case)
        assertion_3_1 = factories.TestCaseAssertF.create(step=step3)
        assertion_3_2 = factories.TestCaseAssertF.create(step=step3)

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


class TestCaseModelTestCase(TestCase):
    def test_run_runs_all_responses(self):
        pass

    def test_run_saves_exceptions(self):
        pass
