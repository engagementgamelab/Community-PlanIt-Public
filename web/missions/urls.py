from django.conf.urls.defaults import *


urlpatterns = patterns('missions.views',
    url(r'^player_created/(?P<slug>.*)/', 'fetch', 
        {'player_submitted_only': True,
         'template': 'missions/mission_playercreated.html',},
        name='mission_playercreated'),
    url(r'^(?P<slug>.*)/', 'fetch', name='mission'),
    #url(r'^$', 'all', name='index'),
)
