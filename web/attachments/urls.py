from django.conf.urls.defaults import *
from web.attachments.views import *

urlpatterns = patterns('web.attachments.views',

    url(r'^(?P<slug>[-\w]+)/$', 'instance', name='instance'),
    url(r'^$', 'all', name='index'),
)
