from django.views.generic.base import TemplateView


class Home(TemplateView):
    template_name = 'fortuitus/fcore/home.html'
