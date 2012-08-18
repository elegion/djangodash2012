from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from fortuitus.fcore.models import Company
from fortuitus.feditor.forms import TestCaseForm
from fortuitus.feditor.models import TestProject, TestCase
from fortuitus.feditor.rights import can_edit_project


def project(request, company, project):
    project = get_object_or_404(TestProject, company__slug=company, slug=project)
    testcases = project.testcases.all()

    testcase = None
    if request.GET.get('testcase'):
        testcase = get_object_or_404(TestCase, project=project, slug=request.GET.get('testcase'))
    elif testcases:
        testcase = testcases[0]

    tc_form = TestCaseForm(instance=testcase)

    if request.POST:
        if request.POST.get('action') == 'add_testcase':
            if not can_edit_project(request.user, project):
                return HttpResponseForbidden()
            tc = TestCase.objects.create(name=TestCase.objects.get_unique_new_name(), project=project)
            return redirect(request.path + '?testcase=%s' % tc.slug)

        tc_form = TestCaseForm(request.POST, instance=testcase)
        if tc_form.is_valid():
            tc_form.save()
            return redirect('.')

    data = {
        'project': project,
        'testcases': testcases,
        'testcase': testcase,
        'tc_form': tc_form,
        'new': request.GET.get('new'),
    }
    return TemplateResponse(request, 'fortuitus/feditor/project.html', data)


def testcase(request, company, project, test):
    testcase = get_object_or_404(TestCase, project__company__slug=company, project__slug=project, slug=test)
    data = {
        'testcase': testcase
    }
    return TemplateResponse(request, 'fortuitus/feditor/testcase.html', data)
