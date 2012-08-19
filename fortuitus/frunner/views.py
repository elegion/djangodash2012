from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from fortuitus.feditor.models import TestProject
from fortuitus.frunner.models import TestRun


def projects(request):
    """
    Lists projects.
    """
    # TODO filter projects visibility.
    # TODO filter projects with no runs.
    projects = TestProject.objects.all()
    context = {'projects': projects}
    return TemplateResponse(request, 'fortuitus/frunner/projects.html',
                            context)


def project_runs(request, project_id):
    """
    Lists all test runs for project.
    """
    project = get_object_or_404(TestProject, pk=project_id)
    runs = project.test_runs.all()
    context = {'project': project,
               'runs': runs}
    return TemplateResponse(request, 'fortuitus/frunner/project_runs.html',
                            context)


def testrun(request, project_id, testrun_id):
    """
    Shows test run details.
    """
    project = get_object_or_404(TestProject, pk=project_id)
    testrun = get_object_or_404(TestRun, pk=testrun_id)
    context = {'project': project,
               'test_case': testrun}
    return TemplateResponse(request, 'fortuitus/frunner/testrun.html',
                            context)
