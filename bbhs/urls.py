from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from django.contrib.auth.views import logout

urlpatterns = patterns('bbhs.views',
    url(r'^$', 'index'),
    url(r'^login/$', 'loginView'),
    url(r'^logout/$', 'logoutView'),

)

urlpatterns += patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^chaperone/', include('chaperone.urls'),),
    url(r'^service/', include('service.urls'),),
)
