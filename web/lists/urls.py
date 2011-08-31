from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
    # Comment on detail
    url(r'^community/(?P<slug>.*)/$', 'lists.views.instance', name='lists_instance'),
    url(r'^following/(?P<id>.*)/$', 'lists.views.following', name='lists_following'),
    url(r'^followers/(?P<id>.*)/$', 'lists.views.followers', name='lists_followers'),
)
