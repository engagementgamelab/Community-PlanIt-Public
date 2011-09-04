from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Need to import all URLs from activities
    url(r"^(?P<id>.*)/overview/", "player_activities.views.overview", name="overview"),
    url(r"^(?P<id>.*)/replay/", "player_activities.views.replay", name="replay"),
    url(r"^(?P<id>.*)/", "player_activities.views.get_activity", name="activity"),
    url(r"^$", "player_activities.views.index", name="all"),
    
)
