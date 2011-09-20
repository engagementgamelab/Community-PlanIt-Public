from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
    url(r'^qs/$', 'affiliations.views.affiliation', name='affiliation'),
    url(r'^$', 'affiliations.views.all', name='affiliations'),
)
