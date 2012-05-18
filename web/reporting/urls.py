from django.conf.urls.defaults import *

urlpatterns = patterns('web.reporting.views',
    url(r'^run-report/(?P<report_name>[-\w]+)/(?P<instance_id>\d+)/$', 'run_report', name='run-report'),
)
