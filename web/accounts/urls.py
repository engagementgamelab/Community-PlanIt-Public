from django.conf.urls.defaults import *
from django.contrib.auth.views import logout
from accounts.views import login
from accounts.forms import AccountAuthenticationForm

urlpatterns = patterns('',
    url(r'^dashboard/', 'web.views.index', name='dashboard'),
    url(r'^notifications/$', 'accounts.views.notifications', name='notifications'),
    url(r'^profile/edit/$', 'accounts.views.edit', name='profile_edit'),
    url(r'^register/$', 'accounts.views.register', name='register'),
    url(r'^forgot/$', 'accounts.views.forgot', name='forgot'),
    url(r'^login/$', login, {'template_name': 'accounts/login.html',
                            'authentication_form': AccountAuthenticationForm}, name='login'),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),

    #url(r"^admin_instance_email/(?P<instance_id>.*)/$", "accounts.views.admin_instance_email", name="admin-instance-email"),
    url(r"^admin_instance_email/$", "accounts.views.admin_instance_email", name="admin-instance-email"),
    url(r"^admin_sendemail/$", "accounts.views.admin_sendemail", name="admin-sendemail"),
)
