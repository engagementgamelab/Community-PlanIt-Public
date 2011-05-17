from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
    (r'^picture/$', 'attachments.views.picture'),
    (r'^video/$', 'attachments.views.video'),
)
