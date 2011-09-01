from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.generic.simple import direct_to_template
from django.conf import settings

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

    (r'^accounts/', include('web.accounts.urls', namespace='accounts', app_name='accounts')),
    (r'^comments/', include('web.comments.urls', namespace='comments', app_name='comments')),
    (r'^missions/', include('web.missions.urls', namespace='missions', app_name='missions')),
    (r'^communities/', include('web.instances.urls', namespace='instances', app_name='instances')),
    (r'^affiliation/', include('web.affiliations.urls', namespace='affiliations', app_name='affiliations')),
    (r'^challenges/', include('web.challenges.urls', namespace='challenges', app_name='challenges')),
    (r'^values/', include('web.values.urls', namespace='values', app_name='values')),
    (r'^lists/', include('web.lists.urls', namespace='lists', app_name='lists')),
    (r'^flags/', include('web.flags.urls', namespace='flags', app_name='flags')),
    (r"^activities/", include("web.player_activities.urls", namespace='activities', app_name='player_activities')),

    # generic content redirect, used for comments and notifications
    url(r'^gr/(\d+)/(.+)/$', 'django.contrib.contenttypes.views.shortcut', name='generic_redirect'),

    # generic content redirect, used for comments and notifications
    url(r'^gr/(\d+)/(.+)/$', 'django.contrib.contenttypes.views.shortcut', name='generic_redirect'),

    # Admin stuff
    (r'^curator/', include('web.curator.urls')),
    (r'^admin/gmapsfield/admin/(?P<file>.*)$', 'gmapsfield.views.serve'),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include("web.admin.urls", namespace='admin')),
    (r'^djadmin/', include(admin.site.urls)),
)
if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^rosetta/', include('rosetta.urls')),
    )
