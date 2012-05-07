from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout

urlpatterns = patterns('web.affiliations.views',
    url(r'^(?P<slug>[-\w]+)/$', 'affiliation', name='affiliation'),
    url(r'^$', 'all', name='affiliations'),
)
