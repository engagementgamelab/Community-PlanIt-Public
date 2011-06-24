from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Need to import all URLs from activities
    (r'^mapit/', include('web.activities.mapit.urls')),
    (r'^thinkfast/', include('web.activities.thinkfast.urls')),
    (r'^othershoes/', include('web.activities.othershoes.urls')),
)
