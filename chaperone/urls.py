from django.conf.urls import patterns, include, url

urlpatterns = patterns('chaperone.views',
    url(r'^$', 'index'),
    url(r'^signup/(?P<eventID>.+)/$', 'signup'),
)
