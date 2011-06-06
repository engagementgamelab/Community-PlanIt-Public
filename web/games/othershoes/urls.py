from django.conf.urls.defaults import *

urlpatterns = patterns('web.games',
    url(r'^(?P<id>\d+)/overview/$', 'othershoes.views.overview', name='games_othershoes_overview'),
    url(r'^(?P<id>\d+)/(?P<user_id>\d+)/comment/$', 'othershoes.views.comment', name='games_othershoes_comment'),
    url(r'^(?P<id>\d+)/$', 'othershoes.views.index', name='games_othershoes_index'),
)
