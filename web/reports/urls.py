from django.conf.urls.defaults import *

urlpatterns = patterns('reports.views',
    url(r'^demographic/$', 'demographic', name='demographic'),
    url(r'^demographic2/$', 'demographic2', name='demographic2'),
    url(r'^comments-popular/$', 'report_comments_popular', name='comments_popular'),
    url(r'^comments-by-activity/$', 'report_comments_by_activity', name='comments_by_activity'),
    url(r'^comments-by-activity2/$', 'report_comments_by_activity2', name='comments_by_activity2'),
)
