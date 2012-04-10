from django.conf.urls.defaults import *

from django.contrib.auth.views import logout

from accounts.views import login
from accounts.forms import AccountAuthenticationForm, RegisterFormOne, RegisterFormTwo, RegistrationWizard

urlpatterns = patterns('',
    url(r'^$', 'web.accounts.views.all', name='all'),
    url(r'^dashboard/', 'web.views.index', name='dashboard'),
    url(r'^notifications/$', 'web.accounts.views.notifications', name='notifications'),
    url(r'^profile/edit/', 'web.accounts.views.edit', name='profile_edit'),
    url(r'^register/', RegistrationWizard([RegisterFormOne, RegisterFormTwo]), name='register'),
    url(r'^forgot/', 'web.accounts.views.forgot', name='forgot'),
    url(r'^login/', login, {'template_name': 'accounts/login.html',
                            'authentication_form': AccountAuthenticationForm}, name='login'),
    url(r'^logout/', logout, {'next_page': '/'}, name='logout'),
    url(r"^admin_instance_email/$", "web.accounts.views.admin_instance_email", name="admin-instance-email"),
    url(r"^admin_sendemail/$", "web.accounts.views.admin_sendemail", name="admin-sendemail"),
)
