from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'bbhs.views.index'),
    url(r'^chaperone/', include('chaperone.urls'),),
    url(r'^service/', include('service.urls'),),
)
