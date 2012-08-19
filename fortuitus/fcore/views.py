from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.template.response import TemplateResponse

from fortuitus.fcore import forms


def home(request):
    """ Home page. """
    return TemplateResponse(request, 'fortuitus/fcore/home.html')


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
    if request.user.is_anonymous():
        params = dict(username='demo', password='demo')
        # We can't use get_or_create because we have to use `create_user`.
        try:
            user = User.objects.get(username=params['username'])
        except User.DoesNotExist:
            user = User.objects.create_user(**params)
        user = auth.authenticate(**params)
        auth.login(request, user)
    return redirect('feditor_project', company='demo', project='twitter')
