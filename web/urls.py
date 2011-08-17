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
    url(r'^about/', direct_to_template, {'template': 'static/about.html'}, 'about'),
    url(r'^contact/', direct_to_template, {'template': 'static/contact.html'}, 'contact'),
    url(r'^privacy/', direct_to_template, {'template': 'static/privacy.html'}, 'privacy'),
    url(r'^terms/', direct_to_template, {'template': 'static/terms.html'}, 'terms'),

    # NOTE: Player related
    (r'^player/follow/(?P<id>.*)/$', 'web.accounts.views.follow'),
    (r'^player/unfollow/(?P<id>.*)/$', 'web.accounts.views.unfollow'),
    url(r'^player/(?P<id>.*)/$', 'web.accounts.views.profile', name='accounts_profile'),

    # NOTE: Fixed to singular
    url(r'^$', 'web.views.index', 'home'),
    url(r'^dashboard/$', 'web.views.index', name='dashboard'),
    (r'^account/', include('web.accounts.urls', namespace='accounts', app_name='accounts')),
    (r'^comment/', include('web.comments.urls', namespace='comments', app_name='comments')),
    (r'^mission/', include('web.missions.urls', namespace='missions', app_name='missions')),
    (r'^neighborhood/', include('web.instances.urls', namespace='neighborhood', app_name='instances')),
    (r'^affiliation/', include('web.affiliations.urls', namespace='affiliations', app_name='affiliations')),
    (r'^challenge/', include('web.challenges.urls', namespace='challenges', app_name='challenges')),
    (r'^game/', include('web.games.urls', namespace='games', app_name='games')),
    (r'^value/', include('web.values.urls', namespace='values', app_name='values')),
    (r'^list/', include('web.lists.urls', namespace='lists', app_name='lists')),
    (r'^flag/', include('web.flags.urls', namespace='flags', app_name='flags')),
    (r"^activity/", include("web.player_activities.urls", namespace='activities', app_name='activities')),

    # Admin stuff
    (r'^curator/', include('web.curator.urls')),
    (r'^admin/gmapsfield/admin/(?P<file>.*)$', 'gmapsfield.views.serve'),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include("web.admin.urls")),
    (r'^adm/', include(admin.site.urls)),
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
