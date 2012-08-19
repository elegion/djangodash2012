from django.conf.urls import patterns, url


urlpatterns = patterns('fortuitus.feditor.views',
    url(r'^(?P<company_slug>[\w\d_-]+)/projects/(?P<project_slug>[\w\d_-]+)/edit/$',
        'project', name='feditor_project'),
)
