from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('fortuitus.fcore.urls')),
    url(r'', include('fortuitus.feditor.urls')),
    url(r'', include('fortuitus.frunner.urls')),
)
