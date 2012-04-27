from django.conf.urls.defaults import *

urlpatterns = patterns('comments.views',
    url(r'^flag/(?P<id>.*)/$', 'flag', name='flag'),
    # deprecated. ajax only now
    #url(r'^like/(?P<id>.*)/$', 'like', name='like'),
    url(r'^ajax/like/(?P<id>.*)/$', 'ajax_like', name='ajax_like'),
    url(r'^reply/(?P<id>.*)/$', 'reply', name='reply'),
    url(r'^edit/(?P<id>.*)/$', 'edit', name='edit'),
    url(r'^attachment/remove/(?P<id>.*)/(?P<comment_id>.*)/$', 'remove_attachment', name='remove_attachment'),

    url(r'^ajax/create/', 'ajax_create', name='ajax-create'),
)
