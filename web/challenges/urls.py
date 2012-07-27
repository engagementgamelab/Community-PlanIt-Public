from django.conf.urls.defaults import *
from django.template.defaultfilters import slugify
from .models import Challenge
from .forms import SelectNewActivityForm, NewActivityWizard

single_response_slug = Challenge.get_display_type_by_const(Challenge.SINGLE_RESPONSE)
multi_response_slug = Challenge.get_display_type_by_const(Challenge.MULTI_RESPONSE)
map_slug = Challenge.get_display_type_by_const(Challenge.MAP)
empathy_slug = Challenge.get_display_type_by_const(Challenge.EMPATHY)

urlpatterns = patterns('challenges.views',
    url(r'^$', 'activities.challenge_list_view', name='challenges'),
    #url(r"^(?P<mission_slug>[-\w]+)/new/$",
    #    NewActivityWizard.as_view([SelectNewActivityForm,]),
    #    name = "new"),

    url(r"^"+single_response_slug+"/(?P<challenge_id>\d+)/play/$",
            "single_response.single_response_play_view", 
            name="single-response-play",
    ),
    url(r"^"+single_response_slug+"/(?P<challenge_id>\d+)/overview/$",
            "single_response.single_response_detail_view", 
            name="single-response-overview",
    ),
    url(r"^"+multi_response_slug+"/(?P<challenge_id>\d+)/play/$",
            "multi_response.multi_response_play_view", 
            name="multiple-responses-play",
    ),
    url(r"^"+multi_response_slug+"/(?P<challenge_id>\d+)/overview/$",
            "multi_response.multi_response_detail_view", 
            name="multiple-responses-overview",
    ),
    url(r"^"+map_slug+"/(?P<challenge_id>\d+)/play/$",
            "map.map_play_view", 
            name="map-play",
    ),
    url(r"^"+map_slug+"/(?P<challenge_id>\d+)/overview/$",
            "map.map_detail_view", 
            name="map-overview",
    ),
    url(r"^"+empathy_slug+"/(?P<challenge_id>\d+)/play/$",
            "empathy.empathy_play_view", 
            name="empathy-play",
    ),
    url(r"^"+empathy_slug+"/(?P<challenge_id>\d+)/overview/$",
            "empathy.empathy_detail_view", 
            name="empathy-overview",
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
