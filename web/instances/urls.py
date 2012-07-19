from django.conf.urls.defaults import *

from accounts.views import login, register
from accounts.forms import AccountAuthenticationForm
from instances.views import InstanceList #, InstanceDetail

urlpatterns = patterns('accounts.views',
    url(r'^(?P<game_slug>[-\w]+)/login/$', login, {'template_name': 'accounts/login.html',
                            'authentication_form': AccountAuthenticationForm}, name='login'),
    url(r'^(?P<game_slug>[-\w]+)/join/$', register, name='join'),
    url(r'^(?P<game_slug>[-\w]+)/profile/edit/$', 'edit', name='profile_edit'),
)

urlpatterns += patterns('instances.views',

    url(r'^$', InstanceList.as_view(), name='instances'),
    #url(r'^(?P<slug>[-\w]+)/$', InstanceDetail.as_view(), name='instance'),

    # temporarily putting activity stream (what's happening) and leaderboard (check the standings) here...
    #url(r'^news/$', 'stream', name='stream'),
    #url(r'^leaderboard/$', 'leaderboard', name='leaderboard'),


)
