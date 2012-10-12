from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout

from web.causes.views import sponsor_list_view

urlpatterns = patterns('causes.views',
    url(r'^causes/$', 'cause_list_view', name='cause_list'),
    url(r'^causes/(?P<id>\d+)/$', 'cause_game_detail_view', name='cause_detail_game'),
    url(r'^causes/p/(?P<id>\d+)/$', 'cause_public_detail_view', name='cause_detail_public'),
    url(r'^causes/add/$', 'cause_add_view', name='cause_add'),

    url(r'^coins/$', 'coins_view', name='coins'),
    url(r'^sponsors/$', 'sponsor_list_view', name='sponsor_list'),
)
