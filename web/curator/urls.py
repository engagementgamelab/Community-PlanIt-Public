from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^instance/(?P<id>.*)', 'curator.views.instance'),
    (r'^all_flagged/$', 'curator.views.all_flagged'),
    (r'^all_attachments/$', 'curator.views.all_attachments'),
    (r'^instances/', 'curator.views.all_instances'),
    #(r'^set_pk/', 'curator.views.set_pk'),
    (r'^csv/(?P<model>.*)', 'curator.views.generate_csv'),
)
