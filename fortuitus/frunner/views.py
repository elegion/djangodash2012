from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.utils import simplejson

from fortuitus.fcore.models import Company
from fortuitus.feditor.models import TestProject
from fortuitus.frunner.models import TestRun, TestResult
from fortuitus.frunner.tasks import run_tests


def project_runs(request, company_slug, project_slug):
    """
    Lists all test runs for project.
    """
    company = get_object_or_404(Company, slug=company_slug)
    project = get_object_or_404(TestProject, slug=project_slug)
    runs = project.test_runs.all()
    context = {'company': company,
               'project': project,
               'runs': runs}
    return TemplateResponse(request, 'fortuitus/frunner/project_runs.html',
                            context)


def testrun(request, company_slug, project_slug, testrun_number,
            testcase_slug=None):
    """
    Shows test run details.
    """
    company = get_object_or_404(Company, slug=company_slug)
    project = get_object_or_404(TestProject, slug=project_slug)
    testrun = get_object_or_404(project.test_runs, pk=testrun_number)
    if testcase_slug:
        testcase = get_object_or_404(testrun.testcases, slug=testcase_slug)
    else:
        try:
            testcase = testrun.testcases.all()[0]
        except IndexError:
            testcase = None

    context = {'company': company,
               'project': project,
               'testrun': testrun,
               'testcase': testcase}
    if request.is_ajax():
        html = ''
        if testcase and testcase.result_str() != TestResult.pending and request.GET.get('html'):
            html = TemplateResponse(request, 'fortuitus/frunner/_testcase.html', context).rendered_content
        return HttpResponse(simplejson.dumps({
            'testrun_status': testrun.result_str(),
            'testcase_status': testcase and testcase.result_str() or '',
            'testcase_statuses': dict([(unicode(r.pk), r.result_str()) for r in testrun.testcases.all()]),
            'html': html
        }), mimetype='application/json')
    else:
        return TemplateResponse(request, 'fortuitus/frunner/testrun.html', context)


# TODO: @require_POST (or render template with form on GET)
def run_project(request, company_slug, project_slug):
    """ Creates new TestRun, runs it in celery task, redirects to created TestRun page
    """
    project = get_object_or_404(TestProject, slug=project_slug)
    testrun = TestRun.create_from_project(project)
    run_tests.delay(testrun.pk)
    return redirect('frunner_testrun',
                    company_slug=company_slug,
                    project_slug=project.slug,
                    testrun_number=testrun.pk)
