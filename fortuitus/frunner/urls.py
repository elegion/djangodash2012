from django.conf.urls import patterns, url

from fortuitus.frunner import views


urlpatterns = patterns('',
    url(r'^projects/$', views.projects, name='frunner_projects'),
    url(r'^projects/(?P<project_id>\d+)/$', views.project_runs,
        name='frunner_project_runs'),
    url(r'^projects/(?P<project_id>\d+)/(?P<testrun_id>\d+)/$',
        views.testrun, name='frunner_testrun'),
    url(r'^projects/(?P<project_id>\d+)/run$', views.run_project,
        name='frunner_run_project'),
)
