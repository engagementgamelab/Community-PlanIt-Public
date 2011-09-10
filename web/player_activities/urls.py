from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Need to import all URLs from activities
    url(r"^$", "player_activities.views.index", name="all"),
    url(r"^(?P<id>\d+)/$", "player_activities.views.get_activity", name="activity"),
    url(r"^(?P<id>\d+)/overview/$", "player_activities.views.overview", name="overview"),
    url(r"^(?P<id>\d+)/replay/$", "player_activities.views.replay", name="replay"),
    
)
