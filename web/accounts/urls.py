from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
    url(r'^dashboard/', 'web.views.index', name='accounts_dashboard'),
    url(r'^profile/edit/', 'accounts.views.edit', name='accounts_profile_edit'),
    url(r'^register/', 'accounts.views.register', name='accounts_register'),
    url(r'^forgot/', 'accounts.views.forgot', name='accounts_forgot'),
    url(r'^login/', login, {'template_name': 'accounts/login.html'}, name='accounts_login'),
    url(r'^logout/', logout, {'next_page': '/'}, name='accounts_logout'),
)
