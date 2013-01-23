from django.conf.urls import patterns, include, url

short = '(?P<short>.{6})'

urlpatterns = patterns('shortener.views',
    url(r'^$', 'index'),
    url(r'^thanks/%s/$' % short, 'thanks'),
)
