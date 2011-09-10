from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Need to import all URLs from activities
    url(r"^$", "player_activities.views.index", name="all"),
    url(r"^(?P<id>\d+)/$", "player_activities.views.activity", name="activity"),
    url(r"^empathy/(?P<id>\d+)/$", "player_activities.views.empathy_activity", name="empathy-activity"),
    url(r"^(?P<id>\d+)/overview/$", "player_activities.views.overview", name="overview"),
    url(r"^(?P<id>\d+)/replay/$", "player_activities.views.replay", name="replay"),
    
)
