from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout

urlpatterns = patterns('web.instances.views',
    url(r'^(?P<slug>[-\w]+)/$', 'region', name='instance'),
    url(r'^$', 'all', name='instances'),
    url(r'^(?P<slug>[-\w]+)/affiliations/$', 'affiliations_all', name='affiliations'),
    url(r'^(?P<slug>[-\w]+)/affiliations/qs/$', 'affiliation', name='affiliation'),

)
