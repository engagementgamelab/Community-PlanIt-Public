from django.conf.urls.defaults import *

urlpatterns = patterns('web.games',
    (r'^(?P<id>.*)/overview/$', 'thinkfast.views.overview'),
    (r'^(?P<id>.*)/(?P<user_id>.*)/comment/$', 'thinkfast.views.comment'),
    (r'^(?P<id>.*)/(?P<user_id>.*)/$', 'thinkfast.views.response'),
    (r'^(?P<id>.*)/$', 'thinkfast.views.index'),
)
