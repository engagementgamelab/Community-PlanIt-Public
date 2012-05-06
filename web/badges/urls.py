from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('web.badges.views',
    url(r'^all/$', 'all', name='all'),
)
