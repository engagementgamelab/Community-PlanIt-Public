from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^flag/(?P<id>.*)/', 'web.comments.views.flag'),
    (r'^reply/(?P<id>.*)/', 'web.comments.views.reply'),
)
