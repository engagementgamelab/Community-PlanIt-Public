from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
    # Comment on detail
    (r'^neighborhood/(?P<slug>.*)/$', 'lists.views.instance'),
    (r'^following/(?P<id>.*)/$', 'lists.views.following'),
    (r'^followers/(?P<id>.*)/$', 'lists.views.followers'),
)
