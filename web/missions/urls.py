from django.conf.urls.defaults import *

urlpatterns = patterns('missions.views',
    url(r'^player_created/(?P<slug>.*)/$', 'mission_detail_player_created_view', 
        {'player_submitted_only': True,
         'template': 'missions/mission_playercreated.html',}, name='mission_playercreated'),

    # the order of the two following patterns matters. not sure why...
    url(r'^(?P<mission_id>\d+)/demographic/$', 'mission_detail_with_demographic_form_view', name='mission-with-demographic-form'),
    url(r'^(?P<mission_id>\d+)/$', 'mission_detail_view', name='mission'),

    (r'^(?P<mission_id>\d+)/challenges/', include("challenges.urls", namespace='challenges', app_name='challenges')),
)
