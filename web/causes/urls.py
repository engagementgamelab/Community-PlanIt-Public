from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout

urlpatterns = patterns('causes.views',
    url(r'^bank/$', 'cause_list_view', name='bank'),
    
    url(r'^(?P<id>\d+)/$', 'cause_game_detail_view', name='detail_game'),

    url(r'^(?P<id>\d+)/$', 'cause_public_detail_view', name='detail_public'),

    # url(r'^spend/$', 'causes.views.spend', name='spend'),

    # url(r'^take/(?P<id>\d+)/$', 'causes.views.take', name='take'),

    # url(r'^(?P<id>\d+)/$', 'causes.views.detail', name='detail'),
)
