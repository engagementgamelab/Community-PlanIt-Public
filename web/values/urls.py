from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout

urlpatterns = patterns('values.views',
    url(r'^bank/$', 'cause_list_view', name='bank'),
    
    url(r'^(?P<id>\d+)/$', 'cause_game_detail_view', name='detail_game'),

    url(r'^(?P<id>\d+)/$', 'cause_public_detail_view', name='detail_public'),

    # url(r'^spend/$', 'values.views.spend', name='spend'),

    # url(r'^take/(?P<id>\d+)/$', 'values.views.take', name='take'),

    # url(r'^(?P<id>\d+)/$', 'values.views.detail', name='detail'),
)
