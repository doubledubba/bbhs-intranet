from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('intranet.views',
    url(r'^$', 'index'),
    url(r'^login/$', 'loginView'),
    url(r'^logout/$', 'logoutView'),
    url(r'^user/(?P<username>.+)/$', 'userPage'),
    url(r'^user/(?P<username>.+)/temp$', 'temp'),


)

urlpatterns += patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^chaperone/', include('chaperone.urls'),),
    url(r'^service/', include('service.urls'))
)

short = '(?P<short>.{6})'
urlpatterns += patterns('shortener.views',
    url(r'^shortener/', 'index'),
    url(r'^thanks/%s/$' % short, 'thanks'),
    url(r'^%s$' % short, 'activate'),

)

