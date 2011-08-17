from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
    (r'^(?P<slug>.*)/$', 'instances.views.region'),
    (r'^$', 'instances.views.all', name="index"),
)
