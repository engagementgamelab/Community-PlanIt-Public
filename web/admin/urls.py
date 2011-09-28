from django.conf.urls.defaults import *

from admin.views import delete_obj

urlpatterns = patterns("",
        #url(r"^$", "admin.views.index", name="admin-base"),

        url(r"^$", "admin.views.instance.manage", name="admin-base"),

        url(r"^instance/new/", "admin.views.instance.new", name="instance-new"),
        url(r"^instance/(?P<instance_id>\d+)/edit/", "admin.views.instance.instance", name="instance-edit"),
        url(r"^instance/(?P<id>\d+)/delete/", delete_obj, dict(model='instances.Instance'), name="instance-delete"
        ),

        #url(r"^instance/email/(?P<instance_id>.*)/", "admin.views.instance_email", name="instance-email"),
        #url(r"^instance/sendemail/", "admin.views.sendemail", name="admin-sendemail"),

        url(r"^instance/(?P<instance_id>\d+)/values/$", "admin.views.value.manage", name="manage-values"),
        url(r"^instance/(?P<instance_id>\d+)/value/new/$", "admin.views.value.value", name="value-new"),
        url(r"^instance/(?P<instance_id>\d+)/value/(?P<value_id>\d+)/edit/$", "admin.views.value.value", name="value-edit"),
        url(r"^instance/value/(?P<id>\d+)/delete/$", delete_obj, dict(model='values.Value'), name="value-delete"),

        url(r"^instance/(?P<instance_id>\d+)/missions/$", "admin.views.mission.manage", name="manage-missions"),
        url(r"^instance/(?P<instance_id>\d+)/mission/new/$", "admin.views.mission.mission", name="mission-new"),
        url(r"^instance/(?P<instance_id>\d+)/mission/(?P<mission_id>\d+)/edit/$", "admin.views.mission.mission", name="mission-edit"),
        url(r"^instance/mission/(?P<id>\d+)/delete/$", delete_obj, dict(model='missions.Mission'), name="mission-delete"),

        url(r"^mission/(?P<mission_id>\d+)/activity/$", "admin.views.activity.manage", name="manage-activities"),
        url(r"^mission/(?P<mission_id>\d+)/activity/new/$", "admin.views.activity.activity", name="activity-new"),
        url(r"^mission/(?P<mission_id>\d+)/activity/(?P<activity_id>\d+)/edit/$", "admin.views.activity.activity", name="activity-edit"),
        url(r"^mission/activity/(?P<id>\d+)/delete/$", delete_obj, dict(model='player_activity.PlayerActivity'), name="activity-delete"),
        
        url(r"^activity/(?P<activity_id>\d+)/answer/$", "admin.views.answer.manage", name="manage-answers"),
        url(r"^activity/(?P<activity_id>\d+)/answer/new/$", "admin.views.answer.answer", name="answer-new"),
        url(r"^activity/(?P<activity_id>\d+)/answer/(?P<answer_id>\d+)/edit/$", "admin.views.answer.answer", name="answer-edit"),
        url(r"^activity/answer/(?P<id>\d+)/delete/$", delete_obj, dict(model='answers.Answer', is_translatable=False), name="answer-delete"),        
        url(r'^activity/(?P<activity_id>\d+)/answer/(?P<answer_id>\d+)/comment/(?P<comment_id>\d+)/', 
                                       'admin.views.answer.comment_edit', name='answer-comment-edit'),

        #url(r"^missionorder/(?P<instance_id>.*)/", "admin.views.mission_order", name="mission-order"),
)
