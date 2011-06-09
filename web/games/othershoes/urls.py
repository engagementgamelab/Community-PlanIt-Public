from django.conf.urls.defaults import *

urlpatterns = patterns('web.games',
    url(r'^(?P<id>\d+)/$', 'othershoes.views.index', name='games_othershoes_index'),
    url(r'^(?P<id>\d+)/overview/$', 'othershoes.views.overview', name='games_othershoes_overview'),
    url(r'^(?P<id>.*)/(?P<user_id>.*)/$', 'othershoes.views.response', name='games_othershoes_response'),
)
