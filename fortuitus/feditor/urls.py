from django.conf.urls import patterns, url


urlpatterns = patterns('fortuitus.feditor.views',
    url(r'^(?P<company>[\w\d-]+)/(?P<project>[\w\d-]+)/$', 'project', name='feditor_project'),
)
