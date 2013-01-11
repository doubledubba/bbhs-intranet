from django.conf.urls import patterns, include, url

urlpatterns = patterns('chaperone.views',
    url(r'^$', 'index'),
    url(r'^eventPage/(?P<eventID>\d+)/$', 'eventPage'),
    url(r'^eventPage/(?P<eventID>\d+)/signUp$', 'signUp'),
    url(r'^removeUser/$', 'removeUser'),
)
