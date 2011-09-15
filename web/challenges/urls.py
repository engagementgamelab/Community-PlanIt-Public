from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
    # Accept
    url(r'^(?P<id>\d+)/accept/$', 'challenges.views.accept', name='accept'),
    # Decline
    url(r'^(?P<id>\d+)/decline/$', 'challenges.views.decline', name='decline'),
    # Comment
    url(r'^(?P<id>\d+)/comment/$', 'challenges.views.comment', name='comment'),

    # Add
    url(r'^add/$', 'challenges.views.add', name='add'),
    url(r'^remove/$', 'challenges.views.delete', name='delete'),
    # Fetch
    url(r'^(?P<id>\d+)/$', 'challenges.views.fetch', name='challenge'),
    # Show all
    url(r'^$', 'challenges.views.all', name='index'),
)
