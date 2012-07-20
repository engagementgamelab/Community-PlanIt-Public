from django.conf.urls.defaults import *

from accounts.views import login, register

from instances.views import (
        InstanceListView,
        InstanceDetailView,
)

urlpatterns = patterns('accounts.views',
    url(r'^(?P<game_slug>[-\w]+)/login/$', login, name='login'),
    url(r'^(?P<game_slug>[-\w]+)/join/$', register, name='join'),
    url(r'^(?P<game_slug>[-\w]+)/profile/edit/$', 'edit', name='profile_edit'),
)

urlpatterns += patterns('instances.views',

    url(r'^$', InstanceListView.as_view(), name='instances'),
    url(r'^(?P<slug>[-\w]+)/$', InstanceDetailView.as_view(), name='instance'),

    # temporarily putting activity stream (what's happening) and leaderboard (check the standings) here...
    #url(r'^news/$', 'stream', name='stream'),
    #url(r'^leaderboard/$', 'leaderboard', name='leaderboard'),


)
