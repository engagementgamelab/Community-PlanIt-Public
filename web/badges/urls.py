from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('web.badges.views',
    url(r'^all/$', direct_to_template, {'template': 'badges/all.html' }, name='all'),
)
