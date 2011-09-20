from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
    # Show all
    url(r'^$', 'values.views.all', name='index'),
    # Spend coin
    url(r'^spend/(?P<id>\d+)/$', 'values.views.spend', name='spend'),
    # Take coin
    url(r'^take/(?P<id>\d+)/$', 'values.views.take', name='take'),
    # Show detail
    url(r'^(?P<id>\d+)/$', 'values.views.detail', name='detail'),
)
