from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
    url(r'^dashboard/', 'web.views.index', name='dashboard'),
    url(r'^notifications/$', 'accounts.views.notifications', name='notifications'),
    url(r'^profile/edit/', 'accounts.views.edit', name='profile_edit'),
    url(r'^register/', 'accounts.views.register', name='register'),
    url(r'^forgot/', 'accounts.views.forgot', name='forgot'),
    url(r'^login/', login, {'template_name': 'accounts/login.html'}, name='login'),
    url(r'^logout/', logout, {'next_page': '/'}, name='logout'),
)
