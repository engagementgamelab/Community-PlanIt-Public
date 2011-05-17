from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
    # Comment on detail
    (r'^(?P<id>.*)/comment/$', 'issues.views.comment'),
    # Show all
    (r'^$', 'issues.views.all'),
    # Spend coin
    (r'^spend/(?P<id>.*)/$', 'issues.views.spend'),
    # Take coin
    (r'^take/(?P<id>.*)/$', 'issues.views.take'),
    # Fetch detail
    (r'^(?P<id>.*)/$', 'issues.views.fetch'),
)
