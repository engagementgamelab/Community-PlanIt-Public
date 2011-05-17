from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^(?P<app>.*)/(?P<id>.*)', 'flags.views.add'),
)
