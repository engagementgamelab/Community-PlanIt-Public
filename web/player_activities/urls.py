from django.conf.urls.defaults import *
from .forms import SelectNewActivityForm
from .views.activities import NewActivityWizard

urlpatterns = patterns('player_activities.views',
    # Need to import all URLs from activities
    #url(r"^$", "index", name="all"),
    url(r"^(?P<mission_slug>[-\w]+)/new/$",
        NewActivityWizard.as_view([SelectNewActivityForm,]),
        name = "new"),
    url(r"^(?P<activity_id>\d+)/$",
            "activities.activity",
            dict(
                model='player_activities.PlayerActivity',
                action='play',
            ),
            "activity"),
    url(r"^(?P<activity_id>\d+)/overview/$",
                        "activities.activity",
                        dict(
                           model='player_activities.PlayerActivity',
                           action='overview',
                        ),
                        "overview"),
    url(r"^(?P<activity_id>\d+)/replay/$",
                        "activities.activity",
                        dict(
                           model='player_activities.PlayerActivity',
                           action='replay',
                        ),
                        "replay"),

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
