from django.conf.urls.defaults import *

urlpatterns = patterns('web.games',
    (r'^(?P<id>.*)/overview/$', 'mapit.views.overview'),
    (r'^(?P<id>.*)/(?P<user_id>.*)/comment/$', 'mapit.views.comment'),
    (r'^(?P<id>.*)/(?P<user_id>.*)/$', 'mapit.views.response'),
    (r'^(?P<id>.*)/$', 'mapit.views.index'),
)
