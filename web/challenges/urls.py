from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
    # Accept
    url(r'^(?P<id>.*)/accept/$', 'challenges.views.accept', name='challenges_accept'),
    # Decline
    url(r'^(?P<id>.*)/decline/$', 'challenges.views.decline', name='challenges_decline'),
    # Comment
    url(r'^(?P<id>.*)/comment/$', 'challenges.views.comment', name='challenges_comment'),
    url(r'^(?P<id>.*)/complete/$', 'challenges.views.complete', name='challenges_complete'),

    # Add
    url(r'^add/$', 'challenges.views.add', name='challenges_add'),
    url(r'^remove/$', 'challenges.views.delete', name='challenges_delete'),
    # Fetch
    url(r'^(?P<id>.*)/$', 'challenges.views.fetch', name='challenges_challenge'),
    # Show all
    url(r'^$', 'challenges.views.all', name='index'),
)
