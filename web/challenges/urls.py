from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
    # Accept
    (r'^(?P<id>.*)/accept/$', 'challenges.views.accept'),
    # Decline
    (r'^(?P<id>.*)/decline/$', 'challenges.views.decline'),
    # Comment
    url(r'^(?P<id>.*)/comment/$', 'challenges.views.comment', name='challenges_comment'),
    (r'^(?P<id>.*)/complete/$', 'challenges.views.complete'),

    # Add
    (r'^add/$', 'challenges.views.add'),
    (r'^remove/$', 'challenges.views.delete'),
    # Fetch
    (r'^(?P<id>.*)/$', 'challenges.views.fetch'),
    # Show all
    url(r'^$', 'challenges.views.all', name='index'),
)
