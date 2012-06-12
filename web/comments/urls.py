from django.conf.urls.defaults import *

urlpatterns = patterns('comments.views',
    url(r'^flag/(?P<id>.*)/$', 'flag', name='flag'),
    url(r'^ajax/like/(?P<id>.*)/$', 'ajax_like', name='ajax_like'),
    url(r'^ajax/create/', 'ajax_create', name='ajax-create'),
)
