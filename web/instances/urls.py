from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
    url(r'^(?P<slug>.*)/$', 'instances.views.region', name='instances_instance'),
    url(r'^$', 'instances.views.all', name='instances'),
)
