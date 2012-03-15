from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout

urlpatterns = patterns('web.crowds.views',
    # Accept
    url(r'^(?P<id>\d+)/accept/$', 'accept', name='accept'),
    # Decline
    url(r'^(?P<id>\d+)/decline/$', 'decline', name='decline'),
    # Comment
    url(r'^(?P<id>\d+)/comment/$', 'comment', name='comment'),

    # Add
    url(r'^rally/$', 'rally', name='rally'),
    url(r'^remove/$', 'delete', name='delete'),
    #Submit Response
    #url(r'^(?P<id>\d+)/$', 'challenge', name='challenge'),
    # Show all
    url(r'^$', 'all', name='index'),
)
