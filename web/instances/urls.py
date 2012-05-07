from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout

urlpatterns = patterns('instances.views',
    # temporarily putting activity stream (what's happening) and leaderboard (check the standings) here...
    url(r'^news/$', 'stream', name='stream'),
    url(r'^leaderboard/$', 'leaderboard', name='leaderboard'),

    url(r'^(?P<slug>[-\w]+)/$', 'region', name='instance'),
    url(r'^$', 'all', name='instances'),
    url(r"^ajax/load-games-by-city/(?P<for_city_id>\d+)/$", "ajax_load_games_by_city", name="ajax-load-games-by-city"),
    url(r"^ajax/load-languages-by-game/(?P<instance_id>\d+)/$", "ajax_load_languages_by_game", name="ajax-load-languages-by-game"),


)
