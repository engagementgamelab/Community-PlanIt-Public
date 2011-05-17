from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
    (r'^dashboard/', 'web.views.index'),
    (r'^profile/edit/', 'accounts.views.edit'),
    (r'^register/', 'accounts.views.register'),
    (r'^forgot/', 'accounts.views.forgot'),
    (r'^login/', login, {'template_name': 'accounts/login.html'}),
    (r'^logout/', logout, {'next_page': '/'}),
)
