from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from fortuitus.feditor.models import TestProject, TestCase


def project(request, company, project):
    project = get_object_or_404(TestProject, company__slug=company, slug=project)
    data = {
        'project': project
    }
    return TemplateResponse(request, 'fortuitus/feditor/project.html', data)


def testcase(request, company, project, test):
    testcase = get_object_or_404(TestCase, project__company__slug=company, project__slug=project, slug=test)
    data = {
        'testcase': testcase
    }
    return TemplateResponse(request, 'fortuitus/feditor/testcase.html', data)
