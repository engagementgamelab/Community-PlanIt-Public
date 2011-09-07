from django.conf.urls.defaults import *
urlpatterns = patterns('',
    url(r'^(?P<slug>.*)/$', 'missions.views.fetch', name='mission'),
    url(r'^$', 'missions.views.all', name='index'),
)
