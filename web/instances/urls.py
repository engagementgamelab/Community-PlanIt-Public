from django.conf.urls.defaults import *

from accounts.views import (
                    login,
                    join,
                    switch_games,
                    game_profile_create_view,
)

urlpatterns = patterns('accounts.views',
    url(r'^(?P<game_slug>[-\w]+)/login/$', login, name='login'),
    url(r'^(?P<game_slug>[-\w]+)/register/$', game_profile_create_view, name='register'),
    url(r'^(?P<game_slug>[-\w]+)/join/$', join, name='join'),
    url(r'^(?P<game_slug>[-\w]+)/switch/$', switch_games, name='switch'),
    url(r'^(?P<game_slug>[-\w]+)/profile/edit/$', 'edit', name='profile_edit'),
)

urlpatterns += patterns('instances.views',

    url(r'^$', 'instance_list_view', name='instances'),
    url(r'^(?P<slug>[-\w]+)/$', 'instance_detail_view', name='instance'),

    # temporarily putting activity stream (what's happening) and leaderboard (check the standings) here...
    #url(r'^news/$', 'stream', name='stream'),
    #url(r'^leaderboard/$', 'leaderboard', name='leaderboard'),


)
