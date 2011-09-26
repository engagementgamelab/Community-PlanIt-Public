from django.conf.urls.defaults import *

urlpatterns = patterns('web.flags.views',
    url(r'^(?P<app>.*)/(?P<id>.*)', 'add', name='add'),
)
