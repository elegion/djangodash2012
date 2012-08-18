from django.conf.urls import patterns, url

from fortuitus.fcore import views


urlpatterns = patterns('',
    url(r'^$', views.Home.as_view(), name='home'),
)
