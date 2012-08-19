from django.contrib import messages, auth
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView

from fortuitus.fcore import forms


class Home(TemplateView):
    """ Home page. """
    template_name = 'fortuitus/fcore/home.html'


def signup(request):
    """ Registration view. """
    if request.user.is_authenticated():
        return redirect('home')
    if request.method == 'POST':
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = auth.authenticate(username=user.username,
                                     password=request.POST['password1'])
            auth.login(request, user)
            messages.success(request, 'Thanks for signing up.')
            return redirect('home')
    else:
        form = forms.RegistrationForm()

    return TemplateResponse(request, 'fortuitus/fcore/registration.html',
                            {'form': form})


def demo(request):
    """ Demo mode. Automatically sign in demo user and show 'em dashboard. """
    # TODO autologin
    return redirect('feditor_project', company='demo', project='twitter')
