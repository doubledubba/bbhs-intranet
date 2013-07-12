from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('intranet.views',
    url(r'^$', 'index'),
    url(r'^login/$', 'loginView'),
    url(r'^logout/$', 'logoutView'),

    url(r'^user/monthly/(?P<username>.+)/$', 'monthlyCron'),
    url(r'^user/daily/(?P<username>.+)/$', 'dailyCron'),
    url(r'^user/pk/$', 'viewPK'),
    url(r'^user/(?P<username>.+)/$', 'userPage'),
    url(r'^ad/(?P<eventPK>.+)/$', 'eventAd'),
    url(r'^signedUp_user/$', 'signedUp_user'),
    url(r'^signedUp_user/(?P<text>.+)/$', 'signedUp_user'),
    url(r'^signedUp_admin/$', 'signedUp_admin'),
    url(r'^signedUp_admin/(?P<text>.+)/$', 'signedUp_admin'),


)

urlpatterns += patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^chaperone/', include('chaperone.urls'),),
)

short = '(?P<short>.{6})'
urlpatterns += patterns('shortener.views',
    url(r'^shortener/', 'index'),
    url(r'^thanks/%s/$' % short, 'thanks'),
    url(r'^%s$' % short, 'activate'),

)

