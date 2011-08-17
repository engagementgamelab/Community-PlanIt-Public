from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout

#TODO: games should be removed as a URL link
urlpatterns = patterns('',
    (r'^(?P<mission_slug>.*)/game/', include('web.games.urls')),
    (r'^(?P<slug>.*)/$', 'missions.views.fetch'),
    url(r'^$', 'missions.views.all', name='index'),
)
