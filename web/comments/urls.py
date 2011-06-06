from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^flag/(?P<id>.*)/', 'web.comments.views.flag', name='comments_flag'),
    url(r'^like/(?P<id>.*)/', 'web.comments.views.like', name='comments_like'),
    url(r'^reply/(?P<id>.*)/', 'web.comments.views.reply', name='comments_reply'),
)
