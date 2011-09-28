from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout

urlpatterns = patterns('web.instances.views',
    url(r'^(?P<slug>.*)/$', 'region', name='instance'),
    url(r'^$', 'all', name='instances'),
)
