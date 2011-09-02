from django.conf.urls.defaults import *

from admin.views import delete_obj

urlpatterns = patterns("",
        #url(r"^$", "admin.views.index", name="admin-base"),

        url(r"^$", "admin.views.instance.manage", name="admin-base"),

        url(r"^instance/new/", "admin.views.instance.new", name="instance-new"),
        url(r"^instance/edit/(?P<instance_id>.*)/", "admin.views.instance.instance", name="instance-edit"),
        url(r"^instance/(?P<id>\d+)/delete/", delete_obj, dict(model='instances.Instance'), name="instance-delete"
        ),

        #url(r"^instance/email/(?P<instance_id>.*)/", "admin.views.instance_email", name="instance-email"),
        #url(r"^instance/sendemail/", "admin.views.sendemail", name="admin-sendemail"),

        url(r"^instance/(?P<instance_id>\d+)/values/$", "admin.views.value.manage", name="manage-values"),
        url(r"^instance/(?P<instance_id>\d+)/value/new/$", "admin.views.value.value", name="value-new"),
        url(r"^instance/(?P<instance_id>\d+)/value/(?P<value_id>\d+)/edit/$", "admin.views.value.value", name="value-edit"),
        url(r"^instance/value/(?P<id>\d+)/delete/$", delete_obj, dict(model='values.Value'), name="value-delete"),

        url(r"^activity/(?P<instance_id>\d+)/$", "admin.views.activity.manage", name="manage-activities"),
        url(r"^activity/(?P<instance_id>\d+)/new/$", "admin.views.activity.new", name="activity-new"),
        url(r"^activity/(?P<instance_id>\d+)/(?P<value_id>\d+)/edit/$", "admin.views.activity.activity", name="activity-edit"),
        url(r"^activity/(?P<activity_id>\d+)/delete/$", "admin.views.activity.delete", name="activity-delete"),


        url(r"^instance/(?P<instance_id>\d+)/missions/$", "admin.views.mission.manage", name="manage-missions"),
        url(r"^instance/(?P<instance_id>\d+)/mission/new/$", "admin.views.mission.mission", name="mission-new"),
        url(r"^instance/(?P<instance_id>\d+)/mission/(?P<mission_id>\d+)/edit/$", "admin.views.mission.mission", name="mission-edit"),
        url(r"^instance/mission/(?P<id>\d+)/delete/$", delete_obj, dict(model='missions.Mission'), name="mission-delete"),


        #url(r"^mission/(?P<instance_id>\d+)/$", "admin.views.mission.manage", name="manage-missions"),
        #url(r"^mission/(?P<instance_id>\d+)/new/$", "admin.views.mission.new", name="mission-new"),
        #url(r"^mission/(?P<instance_id>\d+)/(?P<mission_id>\d+)/edit/$", "admin.views.mission.mission", name="mission-edit"),
        #url(r"^mission/(?P<mission_id>\d+)/delete/$", "admin.views.mission.delete", name="mission-delete"),

        #url(r"^missionorder/(?P<instance_id>.*)/", "admin.views.mission_order", name="mission-order"),
        #url(r"^mission/save/", "admin.views.mission_save", name="mission-save"),
        #url(r"^mission/", "admin.views.mission_base", name="mission-base"),

        #url(r"^activity/save/", "admin.views.activity_save", name="activity-save"),
        #url(r"^activity/", "admin.views.activity_base", name="activity-base"),
        #url(r"^activity/edit/(?P<mission_id>.*)/(?P<activity_id>.*)/", "admin.views.activity_edit", name="activity-edit"),
        #url(r"^activity/new/(?P<mission_id>.*)/", "admin.views.activity_new", name="activity-new"),


)
