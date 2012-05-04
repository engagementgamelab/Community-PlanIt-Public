from django.conf.urls.defaults import *
urlpatterns = patterns('missions.views',
    url(r'^player_created/(?P<slug>.*)/', 'fetch_playercreated', name='mission_playercreated'),
    url(r'^(?P<slug>.*)/', 'fetch', name='mission'),
    #url(r'^$', 'all', name='index'),
)
