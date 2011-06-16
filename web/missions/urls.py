from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout

#TODO: make the games go under /games/ like everything else. 
#Also why is this a slug as oppose to an id like EVERYTHING else?
urlpatterns = patterns('',
    (r'^(?P<mission_slug>.*)/game/', include('web.games.urls')),
    (r'^(?P<slug>.*)/$', 'missions.views.fetch'),
    (r'^$', 'missions.views.all'),
)
