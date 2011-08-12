from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Need to import all URLs from activities
    url(r"^(?P<id>.*)/overview/", "player_activities.views.overview", name="player_activities_overview"),
    url(r"^(?P<id>.*)/", "player_activities.views.get_activity", name="player_activities_activity"),
    url(r"^$", "player_activities.views.index", name="player_activities_all"),
)
