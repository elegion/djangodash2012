from django.views.generic.base import TemplateView


class Home(TemplateView):
    """ Home page. """
    template_name = 'fortuitus/fcore/home.html'
