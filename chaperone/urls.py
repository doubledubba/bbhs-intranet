from django.conf.urls import patterns, include, url

urlpatterns = patterns('chaperone.views',
    url(r'^$', 'index'),
    url(r'^eventPage/(?P<eventID>\d+)/$', 'eventPage'),
    url(r'^eventPage/(?P<eventID>\d+)/signUp$', 'signUp'),
    url(r'^eventPage/(?P<eventID>\d+)/removeChaperone$', 'removeChaperone'),
    url(r'^users/(?P<username>.+)/$', 'userPage'),
)
