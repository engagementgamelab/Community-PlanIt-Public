from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout

urlpatterns = patterns('instances.views',
    # temporarily putting activity stream (what's happening) and leaderboard (check the standings) here...
    url(r'^news/$', 'stream', name='stream'),
    url(r'^leaderboard/$', 'leaderboard', name='leaderboard'),

    url(r'^(?P<slug>[-\w]+)/$', 'region', name='instance'),
    url(r'^$', 'all', name='instances'),
    url(r'^(?P<slug>[-\w]+)/affiliations/$', 'affiliations_all', name='affiliations'),
    url(r'^(?P<instance_slug>[-\w]+)/affiliations/(?P<affiliation_slug>[-\w]+)/$', 'affiliation', name='affiliation'),
    url(r"^ajax/load-games-sijax/(?P<for_city_id>\d+)/$", "load_games_sijax", name="load-games-sijax"),


)
