from django.conf.urls.defaults import *

urlpatterns = patterns('missions.views',
    url(r'^player_created/(?P<slug>.*)/$', 'mission_detail_player_created', 
        {'player_submitted_only': True,
         'template': 'missions/mission_playercreated.html',}, name='mission_playercreated'),

    # the order of the two following patterns matters. not sure why...
    url(r'^(?P<slug>.*)/demographic/$', 'mission_detail_with_demographic_form', name='mission-with-demographic-form'),
    url(r'^(?P<slug>.*)/$', 'mission_detail', name='mission'),
)
