from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.generic.simple import direct_to_template

from web.instances.models import Instance

# Setup admin
admin.autodiscover()

# Override server URLS
handler500 = 'web.views.server_error'

urlpatterns = patterns('',
    url(r'^$', 'web.views.index', name='home'),
    url(r'^about/',
        direct_to_template,
        {
            'template': 'static/about.html',
            'extra_context': {
                'instances': Instance.objects.all
            }
        },
        name='about'
    ),
    url(r'^contact/',
        direct_to_template,
        {
            'template': 'static/contact.html',
            'extra_context': {
                'instances': Instance.objects.all
            }
        },
        name='contact'
    ),
    url(r'^privacy/',
        direct_to_template,
        {
            'template': 'static/privacy.html',
            'extra_context': {
                'instances': Instance.objects.all
            }
        },
        name='privacy'
    ),
    url(r'^terms/',
        direct_to_template,
        {
            'template': 'static/terms.html',
            'extra_context': {
                'instances': Instance.objects.all
            }
        },
        name='terms'
    ),

    url(r'^player/follow/(?P<id>\d+)/$', 'web.accounts.views.follow', name="player_follow"),
    url(r'^player/unfollow/(?P<id>\d+)/$', 'web.accounts.views.unfollow', name="player_unfollow"),
    url(r'^player/(?P<id>\d+)/$', 'web.accounts.views.profile', name='accounts_profile'),

    url(r'^dashboard/$', 'web.views.index', name='dashboard'),
    (r'^accounts/', include('web.accounts.urls')),
    (r'^comments/', include('web.comments.urls')),
    (r'^missions/', include('web.missions.urls')),
    (r'^communities/', include('web.instances.urls')),
    (r'^affiliation/', include('web.affiliations.urls')),
    (r'^challenges/', include('web.challenges.urls')),
    (r'^values/', include('web.values.urls')),
    (r'^lists/', include('web.lists.urls')),
    (r'^flags/', include('web.flags.urls')),
    (r"^activities/", include("web.player_activities.urls")),

    # generic content redirect, used for comments and notifications
    url(r'^gr/(\d+)/(.+)/$', 'django.contrib.contenttypes.views.shortcut', name='generic_redirect'),

    # Admin stuff
    (r'^curator/', include('web.curator.urls')),
    (r'^admin/gmapsfield/admin/(?P<file>.*)$', 'gmapsfield.views.serve'),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include("web.admin.urls")),
    (r'^djadmin/', include(admin.site.urls)),
)
