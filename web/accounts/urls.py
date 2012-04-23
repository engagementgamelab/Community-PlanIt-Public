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


#from accounts.views import login

urlpatterns = patterns('',
    url(r'^logout/', logout, {'next_page': '/'}, name='logout'),
    url(r'^login/$', RegistrationWizard.as_view(
                                            [
                                                RegisterFormOne,
                                                RegisterFormTwo
                                            ]
                                ), name='login'),
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
    #url(r'^login/$', login, {'template_name': 'accounts/login.html',
    #                        'authentication_form': AccountAuthenticationForm}, name='login'),
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
