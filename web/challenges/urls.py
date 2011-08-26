from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
    # Accept
    url(r'^(?P<id>.*)/accept/$', 'challenges.views.accept', name='accept'),
    # Decline
    url(r'^(?P<id>.*)/decline/$', 'challenges.views.decline', name='decline'),
    # Comment
    url(r'^(?P<id>.*)/comment/$', 'challenges.views.comment', name='comment'),

    # Add
    url(r'^add/$', 'challenges.views.add', name='add'),
    url(r'^remove/$', 'challenges.views.delete', name='delete'),
    # Fetch
    url(r'^(?P<id>.*)/$', 'challenges.views.fetch', name='challenge'),
    # Show all
    url(r'^$', 'challenges.views.all', name='index'),
)
