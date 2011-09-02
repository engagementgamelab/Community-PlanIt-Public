from django.conf.urls.defaults import *

urlpatterns = patterns("",
        #url(r"^$", "admin.views.index", name="admin-base"),

        url(r"^$", "admin.views.instance.manage", name="admin-base"),

        url(r"^instance/new/", "admin.views.instance.new", name="instance-new"),
        url(r"^instance/edit/(?P<instance_id>.*)/", "admin.views.instance.instance", name="instance-edit"),
        url(r"^instance/delete/(?P<instance_id>.*)/", "admin.views.instance.delete", name="instance-delete"),

        #url(r"^instance/email/(?P<instance_id>.*)/", "admin.views.instance_email", name="instance-email"),
        #url(r"^instance/sendemail/", "admin.views.sendemail", name="admin-sendemail"),

        url(r"^value/(?P<instance_id>\d+)/$", "admin.views.value.manage", name="manage-values"),
        url(r"^value/(?P<instance_id>\d+)/new/$", "admin.views.value.new", name="value-new"),
        url(r"^value/(?P<instance_id>\d+)/(?P<value_id>\d+)/edit/$", "admin.views.value.value", name="value-edit"),
        url(r"^value/(?P<value_id>\d+)/delete/$", "admin.views.value.delete", name="value-delete"),

        #url(r"^missionorder/(?P<instance_id>.*)/", "admin.views.mission_order", name="mission-order"),
        #url(r"^mission/save/", "admin.views.mission_save", name="mission-save"),
        #url(r"^mission/", "admin.views.mission_base", name="mission-base"),

        #url(r"^activity/save/", "admin.views.activity_save", name="activity-save"),
        #url(r"^activity/", "admin.views.activity_base", name="activity-base"),
        #url(r"^activity/edit/(?P<mission_id>.*)/(?P<activity_id>.*)/", "admin.views.activity_edit", name="activity-edit"),
        #url(r"^activity/new/(?P<mission_id>.*)/", "admin.views.activity_new", name="activity-new"),


)
