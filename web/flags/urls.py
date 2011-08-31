from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^(?P<app>.*)/(?P<id>.*)', 'flags.views.add', name='flags_add'),
)
