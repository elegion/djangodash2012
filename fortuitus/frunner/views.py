from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse

from fortuitus.fcore.models import Company
from fortuitus.feditor.models import TestProject
from fortuitus.frunner.models import TestRun
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
    return TemplateResponse(request, 'fortuitus/frunner/testrun.html',
                            context)


# TODO: @require_POST (or render template with form on GET)
def run_project(request, company_slug, project_slug):
    project = get_object_or_404(TestProject, slug=project_slug)
    testrun = TestRun.create_from_project(project)
    run_tests.delay(testrun.pk)
    return redirect('frunner_testrun',
                    company_slug=company_slug,
                    project_slug=project.slug,
                    testrun_number=testrun.pk)
