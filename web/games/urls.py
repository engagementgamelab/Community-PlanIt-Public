from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Need to import all URLs from sub games
    (r'^mapit/', include('web.games.mapit.urls')),
    (r'^thinkfast/', include('web.games.thinkfast.urls')),
    (r'^othershoes/', include('web.games.othershoes.urls')),
)
