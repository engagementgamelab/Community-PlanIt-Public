from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
<<<<<<< HEAD
    (r'^(?P<slug>.*)/$', 'instances.views.region'),
    (r'^$', 'instances.views.all', name="index"),
=======
    url(r'^(?P<slug>.*)/$', 'instances.views.region', name='instances_instance'),
    url(r'^$', 'instances.views.all', name='instances'),
>>>>>>> 4198bb313e1369a3debcaf37ba0ac3b493bc42a3
)
