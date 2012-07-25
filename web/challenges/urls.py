from django.conf.urls.defaults import *
from .forms import SelectNewActivityForm, NewActivityWizard

urlpatterns = patterns('challenges.views',
    # Need to import all URLs from activities
    #url(r"^$", "index", name="all"),
    url(r"^(?P<mission_slug>[-\w]+)/new/$",
        NewActivityWizard.as_view([SelectNewActivityForm,]),
        name = "new"),

    url(r"^single-response/(?P<challenge_id>\d+)/play/$",
            "activities.single_response_play_view", 
            name="single-response-play",
    ),
    url(r"^single-response/(?P<challenge_id>\d+)/overview/$",
            "activities.single_response_detail_view", 
            name="single-response-overview",
    ),

    #url(r"^(?P<activity_id>\d+)/$",
    #        "activities.activity",
    #        dict(
    #            model='challenges.PlayerActivity',
    #            action='play',
    #        ), "activity"),
    #url(r"^(?P<activity_id>\d+)/overview/$",
    #        "activities.activity",
    #        dict(
    #            model='challenges.PlayerActivity',
    #            action='overview',
    #        ), "overview"),

    #url(r"^empathy/(?P<activity_id>\d+)/$",
    #        "activities.activity",
    #        dict(
    #                model='challenges.PlayerEmpathyActivity',
    #                action='play',
    #        ),
    #        "empathy-activity"),
    #url(r"^empathy/(?P<activity_id>\d+)/overview/$",
    #        "activities.activity",
    #        dict(
    #                model='challenges.PlayerEmpathyActivity',
    #                action='overview',
    #        ),
    #        "empathy-overview"),

    #url(r"^map/(?P<activity_id>\d+)/$", 
    #        "activities.activity", 
    #        dict(
    #                model='challenges.PlayerMapActivity', 
    #                action='play',
    #        ),
    #        "map-activity"),
    #url(r"^map/(?P<activity_id>\d+)/overview/$", 
    #        "activities.activity", 
    #        dict(
    #                model='challenges.PlayerMapActivity', 
    #                action='overview',
    #        ),
    #        "map-overview"),
)
