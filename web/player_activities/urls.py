from django.conf.urls.defaults import *

urlpatterns = patterns('player_activities.views',
    # Need to import all URLs from activities
    #url(r"^$", "index", name="all"),
    url(r"^(?P<id>\d+)/$", "activity.activity", name="activity"),
    url(r"^(?P<id>\d+)/overview/$", "activity.overview", name="overview"),
    url(r"^(?P<id>\d+)/replay/$", "activity.replay", name="replay"),

    #url(r"^empathy/(?P<id>\d+)/$", "empathy.empathy_activity", name="empathy-activity"),
    #url(r"^empathy/(?P<id>\d+)/overview/$", "empathy.empathy_overview", name="empathy-overview"),
    #url(r"^empathy/(?P<id>\d+)/replay/$", "empathy.empathy_replay", name="empathy-replay"),

    url(r"^empathy/(?P<activity_id>\d+)/$", 
                        "activities.activity", 
                        dict(
                                model='player_activities.PlayerEmpathyActivity', 
                                action='play',
                        ),
                        "empathy-activity"),
    url(r"^empathy/(?P<activity_id>\d+)/overview/$", 
                        "activities.activity", 
                        dict(
                                model='player_activities.PlayerEmpathyActivity', 
                                action='overview',
                        ),
                        "empathy-overview"),
    url(r"^empathy/(?P<activity_id>\d+)/replay/$", 
                        "activities.activity", 
                        dict(
                                model='player_activities.PlayerEmpathyActivity', 
                                action='replay',
                        ),
                        "empathy-replay"),

    url(r"^map/(?P<activity_id>\d+)/$", 
                        "activities.activity", 
                        dict(
                                model='player_activities.PlayerMapActivity', 
                                action='play',
                        ),
                        "map-activity"),
    url(r"^map/(?P<activity_id>\d+)/overview/$", 
                        "activities.activity", 
                        dict(
                                model='player_activities.PlayerMapActivity', 
                                action='overview',
                        ),
                        "map-overview"),
    url(r"^map/(?P<activity_id>\d+)/replay/$", 
                        "activities.activity", 
                        dict(
                                model='player_activities.PlayerMapActivity', 
                                action='replay',
                        ),
                        "map-replay"),
    
)
