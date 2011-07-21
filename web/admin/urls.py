from django.conf.urls.defaults import *

urlpatterns = patterns("",
                       url(r"^instance/initial/", "admin.views.instance_initial_index", name="instance-initial-index"),
                       url(r"^instance/initialsave/", "admin.views.instance_initial_save", name="instance-initial-save"),
                       url(r"^instance/sendemail/", "admin.views.sendemail", name="admin-sendemail"),
                       url(r"^instance/save/", "admin.views.instance_save", name="instance-save"),
                       url(r"^instance/", "admin.views.instance_base", name="instance-base"),
                       url(r"^value/initial/", "admin.views.values_initial", name="value-initial"),
                       url(r"^value/save/", "admin.views.values_save", name="value-save"),
                       url(r"^value/", "admin.views.values_base", name="value-base"),
                       url(r"^mission/save/", "admin.views.mission_save", name="mission-save"),
                       url(r"^mission/", "admin.views.mission_base", name="mission-base"),
                       url(r"^activity/save/", "admin.views.activity_save", name="activity-save"),
                       url(r"^activity/", "admin.views.activity_base", name="activity-base"),
                       url(r"^$", "admin.views.index", name="admin-base"),
)
