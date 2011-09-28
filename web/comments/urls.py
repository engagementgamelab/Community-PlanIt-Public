from django.conf.urls.defaults import *

urlpatterns = patterns('comments.views',
    url(r'^flag/(?P<id>.*)/', 'flag', name='flag'),
    url(r'^like/(?P<id>.*)/', 'like', name='like'),
    url(r'^reply/(?P<id>.*)/', 'reply', name='reply'),
    url(r'^edit/(?P<id>.*)/', 'edit', name='edit'),
    url(r'^attachment/remove/(?P<id>.*)/(?P<comment_id>.*)/', 'remove_attachment', name='remove_attachment'),
)
