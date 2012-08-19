from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse

from fortuitus.feditor.forms import TestCaseForm
from fortuitus.feditor.models import TestProject, TestCase, TestCaseStep, TestCaseAssert
from fortuitus.feditor.models_base import method_choices
from fortuitus.feditor.params import Params
from fortuitus.feditor.rights import can_edit_project


def project(request, company_slug, project_slug):
    """ Project page view. """
    project = get_object_or_404(TestProject, company__slug=company_slug,
                                slug=project_slug)
    testcases = project.testcases.all()

    testcase = None
    if request.GET.get('testcase'):
        testcase = get_object_or_404(TestCase, project=project,
                                     slug=request.GET.get('testcase'))
    elif testcases:
        testcase = testcases[0]

    tc_form = TestCaseForm(instance=testcase)

    if request.POST:
        if not can_edit_project(request.user, project):
            return HttpResponseForbidden()

        if request.POST.get('action') == 'add_testcase':
            name = TestCase.objects.get_unique_new_name()
            tc = TestCase.objects.create(name=name, project=project)
            return redirect(request.path + '?testcase=%s' % tc.slug)

        if request.POST.get('action') == 'delete_testcase':
            TestCase.objects.filter(pk=request.POST.get('testcase')).delete()
            return redirect(request.path)

        if request.POST.get('action') in ['save_step', 'add_step']:
            if request.POST.get('action') == 'add_step':
                order = TestCaseStep.objects.filter(testcase=testcase).order_by('-order')
                if order:
                    order = order[0].order + 1
                else:
                    order = 1
                step = [TestCaseStep(testcase=testcase, order=order)]
            else:
                step = TestCaseStep.objects.filter(pk=request.POST.get('teststep'))

            if step:
                step = step[0]
                step.params = Params()
                for param in request.POST:
                    if param.startswith('js_'):
                        step.params[param[3:]] = request.POST[param]
                method = request.POST.get('method')
                url = request.POST.get('url')
                if url:
                    step.url = url
                if method and method in dict(method_choices):
                    step.method = method
                step.save()
            return redirect(request.path + '?testcase=%s' % testcase.slug)

        if request.POST.get('action') == 'delete_step':
            TestCaseStep.objects.filter(pk=request.POST.get('teststep')).delete()
            return redirect(request.path + '?testcase=%s' % testcase.slug)

        if request.POST.get('action') == 'add_assertion':
            lhs = request.POST.get('lhs')
            rhs = request.POST.get('rhs')
            operator = request.POST.get('operator')
            teststep = TestCaseStep.objects.filter(testcase=testcase).order_by('-order')[0]
            order = TestCaseAssert.objects.filter(step=teststep).order_by('-order')
            if order:
                order = order[0].order + 1
            else:
                order = 1
            TestCaseAssert.objects.create(step=teststep,
                lhs=lhs, rhs=rhs, operator=operator, order=order)
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
        'methods': method_choices,
    }
    return TemplateResponse(request, 'fortuitus/feditor/project.html', data)


def testcase(request, company_slug, project_slug, test):
    """ TestCase page view. """
    testcase = get_object_or_404(TestCase,
                                 project__company__slug=company_slug,
                                 project__slug=project_slug,
                                 slug=test)
    data = {
        'testcase': testcase
    }
    return TemplateResponse(request, 'fortuitus/feditor/testcase.html', data)
