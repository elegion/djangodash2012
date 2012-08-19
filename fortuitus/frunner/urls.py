from django.conf.urls import patterns, url

from fortuitus.frunner import views


urlpatterns = patterns('',
    url(r'^(?P<company_slug>[\w\d_-]+)/projects/(?P<project_slug>[\w\d_-]+)/runs/$',
        views.project_runs, name='frunner_project_runs'),
    url(r'^(?P<company_slug>[\w\d_-]+)/projects/(?P<project_slug>[\w\d_-]+)/runs/(?P<testrun_number>\d+)/$',
        views.testrun, name='frunner_testrun'),
    url(r'^(?P<company_slug>[\w\d_-]+)/projects/(?P<project_slug>[\w\d_-]+)/runs/(?P<testrun_number>\d+)/(?P<testcase_slug>[\w\d_-]+)/$',
        views.testrun, name='frunner_testrun'),
    url(r'^(?P<company_slug>[\w\d_-]+)/projects/(?P<project_slug>[\w\d-]+)/run$',
        views.run_project, name='frunner_run_project'),
)
