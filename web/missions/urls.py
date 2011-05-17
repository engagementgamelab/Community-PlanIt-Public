from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
    (r'^(?P<mission_slug>.*)/game/', include('web.games.urls')),
    (r'^(?P<slug>.*)/$', 'missions.views.fetch'),
    (r'^$', 'missions.views.all'),
)
