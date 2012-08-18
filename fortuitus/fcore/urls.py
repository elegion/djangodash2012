from django.conf.urls import patterns, include, url

from fortuitus.fcore import views

urlpatterns = patterns('',
    url(r'^$', views.Home.as_view(), name='home'),
)
