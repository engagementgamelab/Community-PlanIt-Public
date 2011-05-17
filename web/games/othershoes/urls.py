from django.conf.urls.defaults import *

urlpatterns = patterns('web.games',
    (r'^(?P<id>.*)/overview/$', 'othershoes.views.overview'),
    (r'^(?P<id>.*)/(?P<user_id>.*)/comment/$', 'othershoes.views.comment'),
    (r'^(?P<id>.*)/(?P<user_id>.*)/$', 'othershoes.views.response'),
    (r'^(?P<id>.*)/$', 'othershoes.views.index'),
)
