from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
    # Show all
    url(r'^$', 'issues.views.all', name='issues_all'),
    # Spend coin
    url(r'^spend/(?P<id>.*)/$', 'issues.views.spend', name='issues_spend'),
    # Take coin
    url(r'^take/(?P<id>.*)/$', 'issues.views.take', name='issues_take'),
    # Show detail
    url(r'^(?P<id>.*)/$', 'issues.views.detail', name='issues_detail'),
)
