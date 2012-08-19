from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy

from fortuitus.fcore import views


urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {'next_page': reverse_lazy('home')}, name='logout'),
    url(r'^login/$', 'django.contrib.auth.views.login',
        {'template_name': 'fortuitus/fcore/login.html'}, name='login'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^demo/$', views.demo, name='demo'),

    url(r'^(?P<company_slug>[\d\w_-]+)/projects/$', views.projects_list,
        name='fcore_projects_list'),
)
