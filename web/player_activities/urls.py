from django.conf.urls.defaults import *

urlpatterns = patterns('player_activities.views',
    # Need to import all URLs from activities
    #url(r"^$", "index", name="all"),
    url(r"^(?P<id>\d+)/$", "activity.activity", name="activity"),
    url(r"^(?P<id>\d+)/overview/$", "activity.overview", name="overview"),
    url(r"^(?P<id>\d+)/replay/$", "activity.replay", name="replay"),

    url(r"^empathy/(?P<id>\d+)/$", "empathy.empathy_activity", name="empathy-activity"),
    url(r"^empathy/(?P<id>\d+)/overview/$", "empathy.empathy_overview", name="empathy-overview"),
    url(r"^empathy/(?P<id>\d+)/replay/$", "empathy.empathy_replay", name="empathy-replay"),

    url(r"^map/(?P<id>\d+)/$", "map.map_activity", name="map-activity"),
    url(r"^map/(?P<id>\d+)/overview/$", "map.map_overview", name="map-overview"),
    url(r"^map/(?P<id>\d+)/replay/$", "map.map_replay", name="map-replay"),
    
)
