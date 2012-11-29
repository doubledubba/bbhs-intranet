from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('intranet.views',
    url(r'^$', 'index'),
    url(r'^login/$', 'loginView'),
    url(r'^logout/$', 'logoutView'),

)

urlpatterns += patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^chaperone/', include('chaperone.urls'),),
    url(r'^service/', include('service.urls'),),

    (r'^profile/password/$', 'django_ldapbackend.views.password_change'),
    (r'^profile/password/changed/$', 'django.contrib.auth.views.password_change_done'),  
)
