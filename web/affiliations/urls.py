from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
    url(r'^(?P<affiliation>.*)/$', 'affiliations.views.affiliation', name='affiliations_affiliation'),
    url(r'^$', 'affiliations.views.all', name='affiliations'),
)
