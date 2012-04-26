from django.conf.urls.defaults import *
urlpatterns = patterns('missions.views',
    url(r'^(?P<slug>.*)/$', 'fetch', name='mission'),
    #url(r'^$', 'all', name='index'),
)
