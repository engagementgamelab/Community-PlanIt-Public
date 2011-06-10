from django.conf.urls.defaults import *

urlpatterns = patterns('web.games',
    url(r'^(?P<id>\d+)/$', 'thinkfast.views.index', name='games_thinkfast_index'),
    url(r'^(?P<id>\d+)/overview/$', 'thinkfast.views.overview', name='games_thinkfast_overview'),
    url(r'^(?P<id>.*)/(?P<user_id>.*)/$', 'thinkfast.views.response', name='games_thinkfast_response'),
)
