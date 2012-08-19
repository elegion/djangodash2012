import operator

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone
import mock
import requests

from core.factories import ResponseF
from core.tests import BaseTestCase
from fortuitus.feditor import factories as efactories, models as emodels
from fortuitus.frunner import factories as rfactories, models as rmodels
from fortuitus.frunner.tasks import run_tests


class RunTestsTaskTestCase(BaseTestCase):
    def test_non_existing_test(self):
        """
        Should raise emodels.TestCase.DoesNotExist if test case not found.
        """
        with self.assertRaises(rmodels.TestRun.DoesNotExist):
            run_tests(10000)

    @mock.patch('fortuitus.frunner.models.TestRun.run', mock.Mock())
    def test_runs_testcase(self):
        """
        Should call TestRun.run
        """
        testrun = rfactories.TestRunF.create()

        run_tests(testrun.pk)

        rmodels.TestRun.run.assert_called_once_with()


class IntegrationTestCase(BaseTestCase):
    def test_run_tests(self):
        """ Testcases should be passable
        """
        start = timezone.now()

        testcase = rfactories.TestCaseF.create()
        rfactories.TestCaseF.create(testrun=testcase.testrun)
        step1 = rfactories.TestCaseStepF.create(testcase=testcase, order=1)
        step2 = rfactories.TestCaseStepF.create(testcase=testcase, url='groups.json', order=2)
        rfactories.TestCaseAssertF.create(step=step2, lhs='.status_code', rhs='200', operator='eq', order=1)
        rfactories.TestCaseAssertF.create(step=step2, lhs='.text', rhs='Hello, world!', operator='eq', order=2)

        def my_side_effect(*args, **kwargs):
            if args[0] == 'GET' and args[1] == '%s%s' % (testcase.testrun.base_url, step1.url):
                return ResponseF()
            elif args[0] == 'GET' and args[1] == '%s%s' % (testcase.testrun.base_url, step2.url):
                return ResponseF(content='Hello, world!')
            else:
                raise AssertionError('Unexpected requests.request arguments: %s, %s' % (args, kwargs))
        with mock.patch('requests.sessions.Session.request',
                        mock.Mock(side_effect=my_side_effect)):
            run_tests(testcase.testrun.pk)
            self.assertEqual(2, requests.sessions.Session.request.call_count)

        self.assertEqual(1, rmodels.TestRun.objects.count())
        self.assertObject(rmodels.TestRun.objects.all()[0],
                          result=rmodels.TestResult.success)

        self.assertEqual(2, rmodels.TestCase.objects.count())
        self.assertObject(rmodels.TestCase.objects.all()[0],
                          start_date__gte=start,
                          end_date__gte=start,
                          result=rmodels.TestResult.success)
        self.assertObject(rmodels.TestCase.objects.all()[1],
                          start_date__gte=start,
                          end_date__gte=start,
                          result=rmodels.TestResult.success)

    @mock.patch('requests.sessions.Session.request',
                mock.Mock(return_value=ResponseF(status_code=404, content='Wazup!')))
    def test_run_tests2(self):
        """ Test cases should be failable
        """
        start = timezone.now()

        testcase = rfactories.TestCaseF.create()
        rfactories.TestCaseF.create(testrun=testcase.testrun)
        step1 = rfactories.TestCaseStepF.create(testcase=testcase, order=1)
        rfactories.TestCaseAssertF.create(step=step1, lhs='.text', rhs='Wazup!', operator='eq', order=1)
        rfactories.TestCaseAssertF.create(step=step1, lhs='.status_code', rhs='200', operator='eq', order=2)
        step2 = rfactories.TestCaseStepF.create(testcase=testcase, url='groups.json', order=2)
        rfactories.TestCaseAssertF.create(step=step2, lhs='.status_code', rhs='200', operator='eq')
        rfactories.TestCaseAssertF.create(step=step2, lhs='.text', rhs='Hello, world!', operator='eq')

        run_tests(testcase.testrun.pk)

        self.assertEqual(1, requests.sessions.Session.request.call_count)

        self.assertEqual(1, rmodels.TestRun.objects.count())
        self.assertObject(rmodels.TestRun.objects.all()[0],
                          result=rmodels.TestResult.fail)

        self.assertEqual(2, rmodels.TestCase.objects.count())
        self.assertObject(rmodels.TestCase.objects.all()[0],
                          start_date__gte=start,
                          end_date__gte=start,
                          result=rmodels.TestResult.fail)
        self.assertObject(rmodels.TestCase.objects.all()[1],
                          start_date__gte=start,
                          end_date__gte=start,
                          result=rmodels.TestResult.success)
        self.assertEqual(2, rmodels.TestCaseStep.objects.count())
        self.assertObject(rmodels.TestCaseStep.objects.all()[0],
                          result=rmodels.TestResult.fail,
                          exception='AssertionError: 404 should be eq 200')

    @mock.patch('requests.sessions.Session.request', mock.Mock(side_effect=requests.Timeout('bad for you')))
    def test_run_tests3(self):
        """ Testcases can raise errors, and they are handled
        """
        start = timezone.now()

        testcase = rfactories.TestCaseF.create()
        step1 = rfactories.TestCaseStepF.create(testcase=testcase, order=1)
        rfactories.TestCaseAssertF.create(step=step1, lhs='.text', rhs='Wazup!', operator='eq', order=1)
        rfactories.TestCaseAssertF.create(step=step1, lhs='.status_code', rhs='200', operator='eq', order=2)
        step2 = rfactories.TestCaseStepF.create(testcase=testcase, url='groups.json', order=2)
        rfactories.TestCaseAssertF.create(step=step2, lhs='.status_code', rhs='200', operator='eq')
        rfactories.TestCaseAssertF.create(step=step2, lhs='.text', rhs='Hello, world!', operator='eq')

        run_tests(testcase.testrun.pk)

        self.assertEqual(1, requests.sessions.Session.request.call_count)

        self.assertEqual(1, rmodels.TestCase.objects.count())
        self.assertObject(rmodels.TestCase.objects.all()[0],
            start_date__gte=start,
            end_date__gte=start,
            result=rmodels.TestResult.error)
        self.assertEqual(2, rmodels.TestCaseStep.objects.count())
        self.assertObject(rmodels.TestCaseStep.objects.all()[0],
            result=rmodels.TestResult.error,
            exception='Timeout: bad for you')


class TestRunModelTestCase(BaseTestCase):
    def test_create_from_project(self):
        """
        Should copy TestProject and (and all related TestCases, TestCaseSteps,
        etc) and return :model:`frunner.TestRun`.
        """
        test_case = efactories.TestCaseF.create()
        step1 = efactories.TestCaseStepF.create(testcase=test_case)
        step2 = efactories.TestCaseStepF.create(testcase=test_case)
        assertion_2_1 = efactories.TestCaseAssertF.create(step=step2)
        step3 = efactories.TestCaseStepF.create(testcase=test_case)
        assertion_3_1 = efactories.TestCaseAssertF.create(step=step3)
        assertion_3_2 = efactories.TestCaseAssertF.create(step=step3)

        rmodels.TestRun.create_from_project(test_case.project)

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

        test_case.run(test_case.testrun)

        self.assertEqual(2, rmodels.TestCaseStep.run.call_count)
        # TODO: fix test
#        print rmodels.TestCaseStep.run.call_args_list

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

        test_case.run(test_case.testrun)

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

        test_case.run(test_case.testrun)

        self.assertEqual(1, rmodels.TestCaseStep.run.call_count)

        self.assertObjectUpdated(test_case,
                                 start_date__gte=start,
                                 end_date__gte=start,
                                 result=rmodels.TestResult.fail)

    @mock.patch('fortuitus.frunner.models.TestCaseStep.run', mock.Mock(side_effect=Exception('asdf')))
    def test_run_saves_exceptions(self):
        """
        Test case should save exceptions thrown by TestCaseStep.run
        (and mark self as error).
        """
        start = timezone.now()
        test_case = rfactories.TestCaseF.create()
        rfactories.TestCaseStepF.create(testcase=test_case)
        rfactories.TestCaseStepF.create(testcase=test_case)

        test_case.run(test_case.testrun)

        self.assertObjectUpdated(test_case,
                                 start_date__gte=start,
                                 end_date__gte=start,
                                 result=rmodels.TestResult.error)


class TestCaseStepModelTestCase(BaseTestCase):
    @mock.patch('fortuitus.frunner.models.TestCaseAssert.do_assertion', mock.Mock(return_value=False))
    @mock.patch('requests.request', mock.Mock(return_value=ResponseF()))
    def test_run_performs_request(self):
        """
        TestCase.run should perform request, saves result
        then perform all assertions and return response on success.
        """
        start = timezone.now()

        response = requests.request.return_value
        step = rfactories.TestCaseStepF()

        rfactories.TestCaseAssertF(step=step)
        rfactories.TestCaseAssertF(step=step)
        rfactories.TestCaseAssertF(step=step)

        res = step.run(step.testcase.testrun, step.testcase, requests, [])
        requests.request.assert_called_once_with(step.method, '%s%s' % (step.testcase.testrun.base_url, step.url),
                                                 data={}, params={})

        self.assertEqual(3, rmodels.TestCaseAssert.do_assertion.call_count)
        rmodels.TestCaseAssert.do_assertion.assert_called_with([response])
        self.assertEqual(response, res)

        self.assertObjectUpdated(step,
                                 start_date__gte=start,
                                 end_date__gte=start,
                                 result=rmodels.TestResult.success,

                                 response_code=response.status_code,
                                 response_headers=response.headers,
                                 response_body=response.text)

    @mock.patch('fortuitus.frunner.models.TestCaseAssert.do_assertion', mock.Mock())
    @mock.patch('requests.request', mock.Mock(return_value=ResponseF()))
    def test_run_without_assertions(self):
        """
        Test case step should be runnable without TestCaseAssertions (and
        should be success).
        """
        start = timezone.now()

        step = rfactories.TestCaseStepF()

        step.run(step.testcase.testrun, step.testcase, requests, [])

        self.assertEqual(0, rmodels.TestCaseAssert.do_assertion.call_count)

        self.assertObjectUpdated(step,
            start_date__gte=start,
            end_date__gte=start,
            result=rmodels.TestResult.success)

    @mock.patch('fortuitus.frunner.models.TestCaseAssert.do_assertion', mock.Mock(side_effect=AssertionError('qwer')))
    @mock.patch('requests.request', mock.Mock(return_value=ResponseF()))
    def test_run_saves_assertion_exceptions(self):
        """
        Test case step should save exceptions raised by assertion
        """
        step = rfactories.TestCaseStepF()
        rfactories.TestCaseAssertF(step=step)
        rfactories.TestCaseAssertF(step=step)

        res = step.run(step.testcase.testrun, step.testcase, requests, [])
        self.assertFalse(res)

        self.assertEqual(1, rmodels.TestCaseAssert.do_assertion.call_count)

        self.assertObjectUpdated(step,
            result=rmodels.TestResult.fail,
            exception='AssertionError: qwer')

    @mock.patch('fortuitus.frunner.models.TestCaseAssert.do_assertion', mock.Mock(side_effect=AssertionError('qwer')))
    @mock.patch('requests.request', mock.Mock(side_effect=requests.Timeout('Timeout error')))
    def test_run_saves_requests_exception(self):
        """ Test case should save exceptions thrown by requests.request. """
        step = rfactories.TestCaseStepF()
        rfactories.TestCaseAssertF(step=step)
        rfactories.TestCaseAssertF(step=step)

        with self.assertRaises(requests.Timeout):
            step.run(step.testcase.testrun, step.testcase, requests, [])

        self.assertEqual(0, rmodels.TestCaseAssert.do_assertion.call_count)

        self.assertObjectUpdated(step,
            result=rmodels.TestResult.error,
            response_body=None,
            response_headers=None,
            response_code=None,
            exception='Timeout: Timeout error')

    @mock.patch('requests.request', mock.Mock(return_value=ResponseF()))
    def test_run_params_GET(self):
        """ TestStep.run should use TestCase and TestStep params
        If request method is GET, params should be serialized as query string
        """
        testcase = rfactories.TestCaseF()#params={'first_name': 'Alex', 'last_name': 'random:16:l'})
        step = rfactories.TestCaseStepF(testcase=testcase,
                                        method=emodels.models_base.Method.GET,
                                        params={'username': 'alex', 'password': '{random:32:dlL}'})

        step.run(step.testcase.testrun, step.testcase, requests, [])

        requests.request.assert_called_once_with(step.method, ''.join([testcase.testrun.base_url, step.url]),
                                                 data={},
                                                 params={'username': 'alex', 'password': step.resolved_params['password']})

#    def test_run_params_priority(self):
#        """ TestStep.params should have higher priority than TestCase.params
#        """

    @mock.patch('requests.request', mock.Mock(return_value=ResponseF()))
    def test_run_params_POST(self):
        """ TestStep.run should use TestCase and TestStep params
        If request method is POST (PUT), params should be transfered in request body
        """
        testcase = rfactories.TestCaseF()#params={'first_name': 'Alex', 'last_name': 'random:16:l'})
        step = rfactories.TestCaseStepF(testcase=testcase,
                                        method=emodels.models_base.Method.POST,
                                        params={'username': 'alex', 'password': '{random:32:dlL}'})

        step.run(step.testcase.testrun, step.testcase, requests, [])

        requests.request.assert_called_once_with(step.method, ''.join([testcase.testrun.base_url, step.url]),
                                                 data={'username': 'alex', 'password': step.resolved_params['password']},
                                                 params={})


class TestCaseAssertTestCase(TestCase):
    def test_do_assertion(self):
        responses = [{'status_code': '404'}, {'status_code': '200'}]
        a = rmodels.TestCaseAssert()

        a.lhs = '0.status_code'
        a.operator = 'eq'
        a.rhs = '404'
        self.assertTrue(a.do_assertion(responses))

        a.lhs = '.status_code'
        a.operator = 'eq'
        a.rhs = '404'
        with self.assertRaises(AssertionError) as e:
            self.assertFalse(a.do_assertion(responses))
        self.assertEqual('200 should be eq 404', e.exception.message)


class ResolversTestCase(TestCase):
    def test_resolve_operator_short_name(self):
        """ Tests operator resolver with short operator name. """
        from fortuitus.frunner import resolvers
        op = resolvers.resolve_operator('eq')
        self.assertEqual(op, operator.eq)

    def test_resolve_operator_full_name(self):
        """
        Tests operator resolver with full operator name, including module.
        """
        from fortuitus.frunner import resolvers
        op = resolvers.resolve_operator('operator.lt')
        self.assertEqual(op, operator.lt)

    def test_resolve_lhs_last_response(self):
        """ Test lhs resolver: last response, dictionary. """
        from fortuitus.frunner.resolvers import resolve_lhs
        responses = [{'status_code': 404}, {'status_code': 200}]
        self.assertEqual(resolve_lhs('.status_code', responses), 200)

    def test_resolve_lhs_arbitrary_response(self):
        """ Test lhs resolver: arbitrary response, dictionary. """
        from fortuitus.frunner.resolvers import resolve_lhs
        responses = [{'status_code': 404}, {'status_code': 200}]
        self.assertEqual(resolve_lhs('0.status_code', responses), 404)

    def test_resolve_lhs_object(self):
        """ Test lhs resolver: arbitrary response, object. """
        from fortuitus.frunner.resolvers import resolve_lhs
        responses = [type('TestResp', (), {'status_code': 200})]
        self.assertEqual(responses[0].status_code, 200)
        self.assertEqual(resolve_lhs('0.status_code', responses), 200)

    def test_resolve_rhs_plain_value(self):
        """ Test rhs resolver: plain value. """
        from fortuitus.frunner.resolvers import resolve_rhs
        self.assertEqual(resolve_rhs(1, []), 1)
        self.assertEqual(resolve_rhs('foo', []), 'foo')

    def test_resolve_rhs_reference(self):
        """ Test rhs resolver: step reference. """
        from fortuitus.frunner.resolvers import resolve_rhs
        responses = [{'status_code': 404}, {'status_code': 200}]
        self.assertEqual(resolve_rhs('1.status_code', responses), 200)


class RunnerViewsTestCase(TestCase):
    def test_projects(self):
        """ Tests project list page is rendered properly. """
        response = self.client.get(reverse('frunner_projects'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('fortuitus/frunner/projects.html')

    def test_project_runs(self):
        """ Tests project list page is rendered properly. """
        project = efactories.TestProjectF.create()
        url = reverse('frunner_project_runs',
                      kwargs={'project_id': project.id})
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('fortuitus/frunner/project_runs.html')

    def test_test_case(self):
        """ Tests project list page is rendered properly. """
        project = efactories.TestProjectF.create()
        case = rfactories.TestCaseF.create()
        url = reverse('frunner_testrun',
                      kwargs={'project_id': project.pk,
                              'testrun_id': case.testrun_id})
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed('fortuitus/frunner/testrun.html')

    def test_run_project(self):
        case = efactories.TestCaseF.create()
        url = reverse('frunner_run_project',
                      kwargs={'project_id': case.project_id})
        self.assertEqual(0, rmodels.TestRun.objects.count())

        response = self.client.post(url)

        self.assertEqual(1, rmodels.TestRun.objects.count())
        self.assertRedirects(response, reverse('frunner_testrun', args=[case.project_id,
                                                                        rmodels.TestRun.objects.all()[0].pk]))


class RegressionTestCase(BaseTestCase):
    """ Tests for old bugs
    """
    @mock.patch('fortuitus.frunner.models.TestCaseStep.run', mock.Mock(return_value=ResponseF(status_code=404)))
    def test_testcase_4xx_response(self):
        """ Test case should not mark itself as failed if receive response with code >= 400
        """
        test_case = rfactories.TestCaseF.create()
        rfactories.TestCaseStepF.create(testcase=test_case)

        test_case.run(test_case.testrun)

        self.assertEqual(1, rmodels.TestCaseStep.run.call_count)
        self.assertObjectUpdated(test_case,
                                 result=rmodels.TestResult.success)

    def test_test_cases_can_be_duplicated(self):
        """
        Should copy same TestProject twice without raising "primary key must be
        unique" IntegrityError.
        """
        test_case = efactories.TestCaseF.create()
        step = efactories.TestCaseStepF.create(testcase=test_case)
        efactories.TestCaseStepF.create(testcase=test_case)
        efactories.TestCaseAssertF.create(step=step)
        efactories.TestCaseAssertF.create(step=step)

        self.assertEqual(rmodels.TestRun.objects.all().count(), 0)

        rmodels.TestRun.create_from_project(test_case.project)
        self.assertEqual(1, rmodels.TestRun.objects.all().count())
        self.assertEqual(1, rmodels.TestCase.objects.all().count())
        self.assertEqual(2, rmodels.TestCaseStep.objects.all().count())
        self.assertEqual(2, rmodels.TestCaseAssert.objects.all().count())

        rmodels.TestRun.create_from_project(test_case.project)
        self.assertEqual(2, rmodels.TestRun.objects.all().count())
        self.assertEqual(2, rmodels.TestCase.objects.all().count())
        self.assertEqual(4, rmodels.TestCaseStep.objects.all().count())
        self.assertEqual(4, rmodels.TestCaseAssert.objects.all().count())
