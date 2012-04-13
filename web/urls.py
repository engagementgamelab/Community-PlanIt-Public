from django.conf import settings
from django.conf.urls.defaults import include, patterns, url
from django.views.generic.simple import direct_to_template
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin

from web.instances.models import Instance

# Setup admin
admin.autodiscover()

# Override server URLS
handler500 = 'web.views.server_error'

urlpatterns = patterns('web',
    url(r'^$', 'views.index', name='home'),

    url(r'^faq/', direct_to_template, { 'template': 'static/faq.html', 
        #'extra_context': { 'instances': Instance.objects.all } 
        }, name='faq'),
    url(r'^about/', direct_to_template, { 'template': 'static/about.html', 'extra_context': { 'instances': Instance.objects.all } }, name='about'),
    url(r'^contact/', direct_to_template, { 'template': 'static/contact.html', 'extra_context': { 'instances': Instance.objects.all } }, name='contact'),
    url(r'^privacy/', direct_to_template, { 'template': 'static/privacy.html', 'extra_context': { 'instances': Instance.objects.all } }, name='privacy'),
    url(r'^terms/', direct_to_template, { 'template': 'static/terms.html', 'extra_context': { 'instances': Instance.objects.all } }, name='terms'),
    url(r'^how-to-play/', direct_to_template, { 'template': 'static/howtoplay.html', 'extra_context': { 'instances': Instance.objects.all } }, name='howtoplay'),

    url(r'^player/(?P<id>\d+)/$', 'accounts.views.profile', name='accounts_profile'),
    (r'^accounts/', include('accounts.urls', namespace='accounts', app_name='accounts')),
    (r'^attachments/', include('attachments.urls', namespace='attachments', app_name='attachments')),
    (r'^comments/', include('comments.urls', namespace='comments', app_name='comments')),
    (r'^missions/', include('missions.urls', namespace='missions', app_name='missions')),
    (r'^communities/', include('instances.urls', namespace='instances', app_name='instances')),
    (r'^affiliation/', include('affiliations.urls', namespace='affiliations', app_name='affiliations')),
    (r'^challenges/', include('challenges.urls', namespace='challenges', app_name='challenges')),
    (r'^crowds/', include('crowds.urls', namespace='crowds', app_name='crowds')),
    (r'^values/', include('values.urls', namespace='values', app_name='values')),
    (r'^lists/', include('lists.urls', namespace='lists', app_name='lists')),
    (r'^flags/', include('flags.urls', namespace='flags', app_name='flags')),
    (r'^activities/', include("player_activities.urls", namespace='activities', app_name='player_activities')),

    # Admin stuff
    #(r'^curator/', include('curator.urls')),
    (r'^reports/', include('reports.urls', namespace='reports', app_name='reports')),
)



urlpatterns += patterns('',
    url(r'^admin_tools/', include('admin_tools.urls')),
    (r'^admin/gmapsfield/admin/(?P<file>.*)$', 'gmapsfield.views.serve'),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    #(r'^admin/', include("admin.urls", namespace='admin')),
    (r'^admin/', include(admin.site.urls)),
    # generic content redirect, used for comments and notifications
    url(r'^gr/(\d+)/(.+)/$', 'django.contrib.contenttypes.views.shortcut', name='generic_redirect'),
)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^rosetta/$', include('rosetta.urls')),
    )
if 'sentry' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^sentry/$', include('sentry.web.urls')),
    )
urlpatterns += patterns('core.memcached_status',
    url(r'^status/cache/$', 'view'),
)

urlpatterns += staticfiles_urlpatterns()
