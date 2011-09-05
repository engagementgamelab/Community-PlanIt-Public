from django.conf.urls.defaults import *

urlpatterns = patterns("",
        url(r"^$", "admin.views.manage_game", name="admin-base"),
        #url(r"^$", "admin.views.index", name="admin-base"),

        url(r"^instance/new/", "admin.views.instance_new", name="instance-new"),
        url(r"^instance/edit/(?P<instance_id>.*)/", "admin.views.instance", name="instance-edit"),
        url(r"^instance/delete/(?P<instance_id>.*)/", "admin.views.instance_delete", name="instance-delete"),
        url(r"^instance/email/(?P<instance_id>.*)/", "admin.views.instance_email", name="instance-email"),
        url(r"^instance/initial/", "admin.views.instance_initial_index", name="instance-initial-index"),
        url(r"^instance/initialsave/", "admin.views.instance_initial_save", name="instance-initial-save"),
        url(r"^instance/sendemail/", "admin.views.sendemail", name="admin-sendemail"),
        url(r"^instance/save/", "admin.views.instance_save", name="instance-save"),
        #url(r"^instance/manage/base/", "admin.views.instance_manage_base", name="instance-manage-base"),
        url(r"^instance/", "admin.views.instance_base", name="instance-base"),

        url(r"^missionorder/(?P<instance_id>.*)/", "admin.views.mission_order", name="mission-order"),
        url(r"^mission/save/", "admin.views.mission_save", name="mission-save"),
        url(r"^mission/", "admin.views.mission_base", name="mission-base"),

        
        url(r"^value/(?P<instance_id>\d+)/new/", "admin.views.value_new", name="value-new"),
        url(r"^value/(?P<instance_id>\d+)/edit/(?P<value_id>.*)/", "admin.views.value", name="value-edit"),
        url(r"^value/(?P<value_id>\d+)/delete", "admin.views.value_delete", name="value-delete"),
        url(r"^value/(?P<instance_id>\d+)/", "admin.views.manage_values", name="manage-values"),
        
        #url(r"^value/(?P<instance_id>.*)/", "admin.views.values_edit", name="values-edit"),
        url(r"^value/initial/", "admin.views.values_initial", name="value-initial"),
        url(r"^value/save/", "admin.views.values_save", name="value-save"),
        #url(r"^value/", "admin.views.values_base", name="value-base"),

        url(r"^activity/save/", "admin.views.activity_save", name="activity-save"),
        url(r"^activity/", "admin.views.activity_base", name="activity-base"),
        url(r"^activity/edit/(?P<mission_id>.*)/(?P<activity_id>.*)/", "admin.views.activity_edit", name="activity-edit"),
        url(r"^activity/new/(?P<mission_id>.*)/", "admin.views.activity_new", name="activity-new"),


)
