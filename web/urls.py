from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.generic.simple import direct_to_template
from django.conf import settings

# Setup admin
admin.autodiscover()

# Override server URLS
handler500 = 'web.views.error_500'
handler404 = 'web.views.error_404'

urlpatterns = patterns('',
    # NOTE: Static pages
    (r'^about/', direct_to_template, {'template': 'static/about.html'}),
    (r'^contact/', direct_to_template, {'template': 'static/contact.html'}),
    (r'^privacy/', direct_to_template, {'template': 'static/privacy.html'}),
    (r'^terms/', direct_to_template, {'template': 'static/terms.html'}),

    # NOTE: Player related
    (r'^player/follow/(?P<id>.*)/$', 'web.accounts.views.follow'),
    (r'^player/unfollow/(?P<id>.*)/$', 'web.accounts.views.unfollow'),
    url(r'^player/(?P<id>.*)/$', 'web.accounts.views.profile', name='accounts_profile'),

    # NOTE: Fixed to singular
    (r'^$', 'web.views.index'),
    url(r'^dashboard/$', 'web.views.index', name='dashboard'),
    (r'^account/', include('web.accounts.urls')),
    (r'^comment/', include('web.comments.urls')),
    (r'^mission/', include('web.missions.urls')),
    (r'^neighborhood/', include('web.instances.urls')),
    (r'^affiliation/', include('web.affiliations.urls')),
    (r'^challenge/', include('web.challenges.urls')),
    (r'^game/', include('web.games.urls')),
    (r'^challenge/', include('web.challenges.urls')),
    (r'^value/', include('web.values.urls')),
    (r'^list/', include('web.lists.urls')),
    (r'^flag/', include('web.flags.urls')),
    (r"^activity/", include("web.player_activities.urls")),

    # Admin stuff
    (r'^curator/', include('web.curator.urls')),
    (r'^admin/gmapsfield/admin/(?P<file>.*)$', 'gmapsfield.views.serve'),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
)
if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^rosetta/', include('rosetta.urls')),
    )

if getattr(settings, 'DEBUG', True):
    urlpatterns += patterns('',
        (r'^assets/(?P<path>.*)$', 'django.views.static.serve', 
            {'document_root': settings.MEDIA_ROOT}
        ),
    )
