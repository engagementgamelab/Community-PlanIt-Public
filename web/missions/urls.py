from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
    url(r'^(?P<slug>.*)/$', 'missions.views.fetch', name='missions_mission'),
    url(r'^$', 'missions.views.all', name='index'),
)
