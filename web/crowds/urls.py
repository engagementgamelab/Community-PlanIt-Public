from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout

urlpatterns = patterns('web.crowds.views',

    url(r'^(?P<id>\d+)/view/$', 'view_crowd', name='view'),
    url(r'^(?P<id>\d+)/join/$', 'join_crowd', name='join'),
    url(r'^(?P<id>\d+)/leave/$', 'leave_crowd', name='leave'),
    url(r'^(?P<id>\d+)/comment/$', 'comment', name='comment'),
    url(r'^create/$', 'create', name='create'),
    #url(r'^remove/$', 'delete', name='delete'),
    url(r'^$', 'all', name='index'),
    
    # city page versions of these views, hide the city header by passing extra context    # 
        # url(r'^(?P<id>\d+)/view/city/$', 'view', kwargs={'extra_context': {'city_header': True }}, name='city-view'),
        # url(r'^(?P<id>\d+)/join/city/$', 'join', kwargs={'extra_context': {'city_header': True }}, name='city-join'),
        # url(r'^(?P<id>\d+)/leave/city/$', 'leave', kwargs={'extra_context': {'city_header': True }}, name='city-leave'),
        # url(r'^(?P<id>\d+)/rally/city/$', 'create', kwargs={'extra_context': {'city_header': True }}, name='city-rally'),
    url(r'^city/$', 'all', kwargs={'extra_context': {'city_header': True }}, name='city-index'),
)
