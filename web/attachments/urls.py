from django.conf.urls.defaults import *
from web.attachments.views import *

urlpatterns = patterns('web.attachments.views',
    url(r'^post-game/$', 'post_game', name='post-game'),

    url(r'^(?P<slug>[-\w]+)/$', 'index', name='game-rc'),
    url(r'^$', 'index', kwargs={'extra_context': {'city_header': True,}}, name='index'),

    url(r'^resource/(?P<slug>[-\w]+)/(?P<attachment_id>\d+)$', 'attachment', name='game-attachment'),
    url(r'^resource/(?P<attachment_id>\d+)/$', 'attachment', kwargs={
        'extra_context': {
            'city_header': True,
        }
    }, name='attachment'),
)
