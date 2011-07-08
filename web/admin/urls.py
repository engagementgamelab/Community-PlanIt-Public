from django.conf.urls.defaults import *

urlpatterns = patterns("",
                       url(r"^instance/save/", "admin.views.instance_save", name="instance-save"),
                       url(r"^instance/", "admin.views.instance_base", name="instance-base"),  
                       url(r"^$", "admin.views.index", name="instance-index"),
)
