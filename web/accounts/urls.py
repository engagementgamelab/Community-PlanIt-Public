from django.conf.urls.defaults import *
from django.contrib.auth.views import logout

from .forms import (
            AccountAuthenticationForm,
            RegisterFormOne,
            RegisterFormTwo,
            RegistrationWizard,
            FilterPlayersByVariantsForm,
            SearchPlayersByKeywordsForm,
)

urlpatterns = patterns('',
    url(r'^logout/', logout, {'next_page': '/'}, name='logout'),
    # url(r'^login/$', RegistrationWizard.as_view(
    #                                         [
    #                                             RegisterFormOne,
    #                                             RegisterFormTwo
    #                                         ]
    #                             ), name='login'),
    url(r'^register/$', RegistrationWizard.as_view(
                                            [
                                                RegisterFormOne,
                                                RegisterFormTwo
                                            ]
                                ), name='register'),
    url(r'^dashboard/$', 'web.views.index', name='dashboard'),
)

urlpatterns += patterns('accounts.views',
    url(r'^$', 'all', name='all'),
    url(r'^notifications/$', 'notifications', name='notifications'),
    url(r'^profile/edit/$', 'edit', name='profile_edit'),
    url(r'^player/(?P<id>\d+)/$', 'profile', name='player_profile'),
    url(r'^forgot/$', 'forgot', name='forgot'),
    url(r'^login/$', 'login', {
        'template_name': 'accounts/login.html', 
        'authentication_form': AccountAuthenticationForm
    }, name='login'),
    url(r'^ajax/login/$', 'login_ajax', 
                            {'authentication_form': AccountAuthenticationForm},
                                name='login-ajax'),
    url(r'^ajax/search-players-by-kw/$',
            'ajax_search',
            {'search_form': SearchPlayersByKeywordsForm},
            name='ajax-search-players-by-kw'
    ),
    url(r'^ajax/filter-players-by-variants/$',
            'ajax_search',
            {'search_form': FilterPlayersByVariantsForm},
            name='ajax-filter-players-by-variant'
    ),
    #url(r"^admin_instance_email/$", "admin_instance_email", name="admin-instance-email"),
    #url(r"^admin_sendemail/$", "admin_sendemail", name="admin-sendemail"),
)


from accounts.forms import PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.core.urlresolvers import reverse_lazy
urlpatterns += patterns('django.contrib.auth.views', 
    # Forgot Password
    url(r'^password-reset/$', 'password_reset', {
        'template_name': 'accounts/password_reset.html',
        'email_template_name': 'accounts/email/password_reset_email.html',
        'password_reset_form': PasswordResetForm,
        'post_reset_redirect': reverse_lazy('accounts:password_reset_done'),
    }, name='password_reset'),
    url(r'^password-reset-done/$', 'password_reset_done', {
        'template_name': 'accounts/password_reset_done.html',
    }, name='password_reset_done'),
    
    # Reset Password
    url(r'^password-reset-confirm/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 
    'password_reset_confirm', {
        'template_name': 'accounts/password_reset_confirm.html',
        'set_password_form': SetPasswordForm,
        'post_reset_redirect': reverse_lazy('accounts:password_reset_complete'),
    }, name='password_reset_confirm'),
    url(r'^password-reset-complete/$', 'password_reset_complete', {
        'template_name': 'accounts/password_reset_complete.html',
    }, name='password_reset_complete'),
    
    # Change Password
    # url(r'^password-change/$', 'password_change', {
    #     'template_name': 'accounts/password_change_form.html',
    #     'password_change_form': PasswordChangeForm
    # }, name='password_change'),
    # url(r'^password-change-done/$', 'password_change_done', {
    #     'template_name': 'accounts/password_change_done.html',
    # }, name='password_change_done'),
)
