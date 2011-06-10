from django.conf.urls.defaults import *

urlpatterns = patterns('web.games',
    url(r'^(?P<id>\d+)/$', 'mapit.views.index', name='games_mapit_index'),
    url(r'^(?P<id>\d+)/overview/$', 'mapit.views.overview', name='games_mapit_overview'),
    url(r'^(?P<id>.*)/(?P<user_id>.*)/$', 'mapit.views.response', name='games_mapit_response'),
)
