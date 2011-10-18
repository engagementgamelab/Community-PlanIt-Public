from django.conf.urls.defaults import *

urlpatterns = patterns('reports.views',
    url(r'^general/$', 'report_general', name='general'),
    url(r'^comments-popular/$', 'report_comments_popular', name='comments_popular'),
    url(r'^comments-by-activity/$', 'report_comments_by_activity', name='comments_by_activity'),
)
