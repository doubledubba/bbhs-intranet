from django.conf.urls import patterns, include, url

urlpatterns = patterns('chaperone.views',
    url(r'^$', 'index'),
    url(r'^eventPage/(?P<eventID>\d+)/$', 'eventPage'),
    url(r'^eventPage/(?P<eventID>\d+)/signUp$', 'signUp'),
    url(r'^eventPage/(?P<eventID>\d+)/removeUser/$', 'removeUser'),
    url(r'^eventPage/(?P<eventID>\d+)/addNote$', 'addNote'),
    url(r'^eventPage/(?P<eventID>\d+)/handleRegistration$', 'handleRegistration'),

    url(r'^userReport/$', 'userReport'),
    url(r'^userReport/(?P<username>.+)/$', 'userReport'),
)
