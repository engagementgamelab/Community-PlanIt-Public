from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
    (r'^(?P<affiliation>.*)/$', 'affiliations.views.affiliation'),
    (r'^$', 'affiliations.views.all'),
)
