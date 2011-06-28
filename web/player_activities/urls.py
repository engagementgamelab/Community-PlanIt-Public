from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Need to import all URLs from activities
    (r"^(?P<id>.*)/overview/", "player_activities.views.overview"),
    (r"^(?P<id>.*)/", "player_activities.views.getGame"),
    (r"^$", "player_activities.views.index"),
)
