from django.conf.urls import patterns, include, url

urlpatterns = patterns('service.views',
    url(r'^$', 'index'),
)
