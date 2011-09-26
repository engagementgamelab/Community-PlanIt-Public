from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^flag/(?P<id>.*)/', 'web.comments.views.flag', name='flag'),
    url(r'^like/(?P<id>.*)/', 'web.comments.views.like', name='like'),
    url(r'^reply/(?P<id>.*)/', 'web.comments.views.reply', name='reply'),
    url(r'^edit/(?P<id>.*)/', 'web.comments.views.edit', name='edit'),
    url(r'^attachment/remove/(?P<id>.*)/(?P<comment_id>.*)/', 'web.comments.views.remove_attachment', name='remove_attachment'),
)
