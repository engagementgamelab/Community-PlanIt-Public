from django.conf.urls.defaults import *
from web.attachments.views import *

urlpatterns = patterns('web.attachments.views',
    url(r'^(?P<slug>[-\w]+)/$', 'index', name='game-rc'),
    url(r'^$', 'index', name='index'),

    url(r'^(?P<slug>[-\w]+)/(?P<attachment_id>\d+)$', 'attachment', name='game-attachment'),
    url(r'^(?P<attachment_id>\d+)/$', 'attachment', name='attachment'),
)
