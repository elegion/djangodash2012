from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from fortuitus.fcore.models import Company
from fortuitus.feditor.forms import TestCaseForm
from fortuitus.feditor.models import TestProject, TestCase, TestCaseStep
from fortuitus.feditor.params import Params
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
        if not can_edit_project(request.user, project):
            return HttpResponseForbidden()

        if request.POST.get('action') == 'add_testcase':
            tc = TestCase.objects.create(name=TestCase.objects.get_unique_new_name(), project=project)
            return redirect(request.path + '?testcase=%s' % tc.slug)

        if request.POST.get('action') == 'delete_testcase':
            TestCase.objects.filter(pk=request.POST.get('testcase')).delete()
            return redirect(request.path)

        if request.POST.get('action') == 'save_step':
            step = TestCaseStep.objects.filter(pk=request.POST.get('teststep'))
            if step:
                step = step[0]
                step.params = Params()
                for param in request.POST:
                    if param.startswith('js_'):
                        step.params[param[3:]] = request.POST[param]
                step.save()
            return redirect(request.path + '?testcase=%s' % testcase.slug)

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
