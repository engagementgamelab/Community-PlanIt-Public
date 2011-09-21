from django.conf.urls.defaults import *

urlpatterns = patterns('web.curator.views',
    (r'^instance/(?P<id>.*)', 'instance'),
    (r'^all_flagged/$', 'all_flagged'),
    (r'^all_attachments/$', 'all_attachments'),
    (r'^instances/', 'all_instances'),
    (r'^csv/(?P<model>.*)', 'generate_csv'),
)
