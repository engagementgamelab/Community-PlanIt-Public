from django.conf.urls.defaults import *

urlpatterns = patterns('web.games',
    url(r'^(?P<id>.*)/overview/$', 'othershoes.views.overview', name='games_othershoes_overview'),
    url(r'^(?P<id>.*)/(?P<user_id>.*)/comment/$', 'othershoes.views.comment', name='games_othershoes_comment'),
    url(r'^(?P<id>.*)/(?P<user_id>.*)/$', 'othershoes.views.response', name='games_othershoes_response'),
    url(r'^(?P<id>.*)/$', 'othershoes.views.index', name='games_othershoes_index'),
)
