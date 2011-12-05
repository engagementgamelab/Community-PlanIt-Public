from django.conf.urls.defaults import *

urlpatterns = patterns('reports.views',
    url(r'^demographic/$', 'demographic', name='demographic'),
    #url(r'^demographic2/$', 'demographic2', name='demographic2'),
    url(r'^challenges-activity/$', 'challenges_activity', name='challenges_activity'),
    url(r'^comments-popular/$', 'comments_popular', name='comments_popular'),
    #url(r'^comments-by-activity/$', 'report_comments_by_activity', name='comments_by_activity'),
    url(r'^activity-report/$', 'activity_report', name='activity_report'),
    #url(r'^comments-by-activity2-multi/$', 'report_comments_by_activity2_multi', name='comments_by_activity2_multi'),
)
