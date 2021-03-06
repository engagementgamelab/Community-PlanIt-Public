from filebrowser.sites import site

from django.conf import settings
from django.conf.urls.defaults import include, patterns, url
from django.views.generic.simple import direct_to_template
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.contrib import admin

from web.instances.models import Instance

# Setup admin
admin.autodiscover()

# Override server URLS
handler500 = 'web.views.server_error'

urlpatterns = patterns('web',
    url(r'^$', 'views.index', name='home'),

    url(r'games/', include('instances.urls', namespace='instances', app_name='instances')),

    url(r'^faqs/', direct_to_template, { 'template': 'static/faqs.html', 
        #'extra_context': { 'instances': Instance.objects.all } 
        }, name='faqs'),
    url(r'^about/', direct_to_template, { 'template': 'static/about.html', 'extra_context': { 'instances': Instance.objects.all } }, name='about'),
    url(r'^contact/', direct_to_template, { 'template': 'static/contact.html', 'extra_context': { 'instances': Instance.objects.all } }, name='contact'),
    url(r'^privacy/', direct_to_template, { 'template': 'static/privacy.html', 'extra_context': { 'instances': Instance.objects.all } }, name='privacy'),
    url(r'^terms/', direct_to_template, { 'template': 'static/terms.html', 'extra_context': { 'instances': Instance.objects.all } }, name='terms'),
    url(r'^how-to-play/', direct_to_template, { 'template': 'static/howtoplay.html', 'extra_context': { 'instances': Instance.objects.all } }, name='howtoplay'),
    url(r'^features/', direct_to_template, { 'template': 'static/features.html', 'extra_context': { 'instances': Instance.objects.all } }, name='features'),    
    url(r'^bring-cpi-to-you/$', 'views.bringcpi', name='bringcpi'),
    url(r'^bring-cpi-to-you/thanks/', direct_to_template, { 'template': 'static/bringcpi_thanks.html', 'extra_context': {} }, name='bringcpi-thanks'),
    url(r'^404$', direct_to_template, { 'template': '404.html', 'extra_context': {}}, name='404'),
    url(r'^500$', direct_to_template, { 'template': '500.html', 'extra_context': {}}, name='404'),
    url(r'^humans.txt$', direct_to_template, { 'template': 'humans.txt'}, name='humans'),
    url(r'^robots.txt$', direct_to_template, { 'template': 'robots.txt'}, name='robots'),

    (r'^accounts/', include('accounts.urls', namespace='accounts', app_name='accounts')),
    #(r'^resource-center/', include('attachments.urls', namespace='attachments', app_name='attachments')),
    #(r'^comments/', include('comments.urls', namespace='comments', app_name='comments')),
    (r'^affiliations/', include('affiliations.urls', namespace='affiliations', app_name='affiliations')),
    (r'^lists/', include('lists.urls', namespace='lists', app_name='lists')),
    (r'^flags/', include('flags.urls', namespace='flags', app_name='flags')),

    # Admin stuff
    #(r'^curator/', include('curator.urls')),
    (r'^reports/', include('web.reporting.urls', namespace='reporting', app_name='reporting')),
)

if 'web.badges'  in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^badges/', include('badges.urls', namespace='badges', app_name='badges')         ))

#if 'admin_tools' in settings.INSTALLED_APPS:
#    url(r'^admin_tools/', include('admin_tools.urls')),

if 'socialregistration' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^social/', include('socialregistration.urls', namespace = 'socialregistration'))
    )

if 'grappelli' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^grappelli/', include('grappelli.urls')),
    )

if 'filebrowser' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
    url(r'^admin/filebrowser/', include(site.urls)),
    )

urlpatterns += patterns('',
    (r'^admin/gmapsfield/admin/(?P<file>.*)$', 'gmapsfield.views.serve'),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    #(r'^admin/', include("admin.urls", namespace='admin')),
    (r'^admin/', include(admin.site.urls)),
    # generic content redirect, used for comments and notifications
    url(r'^gr/(\d+)/(.+)/$', 'django.contrib.contenttypes.views.shortcut', name='generic_redirect'),
)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('rosetta.views',
    url(r'^rosetta/$', 'home', name='rosetta-home'),
    url(r'^rosetta/pick/$', 'list_languages', name='rosetta-pick-file'), 
        url(r'^rosetta/download/$', 'download_file', name='rosetta-download-file'),
        url(r'^rosetta/select/(?P<langid>[\w\-]+)/(?P<idx>\d+)/$', 'lang_sel', name='rosetta-language-selection'),
    )

if 'ajax_select' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        (r'^ajax_select/', include('ajax_select.urls')),
    )

if 'django_su' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r"^su/", include("django_su.urls")),
    )

if 'attachments' in settings.INSTALLED_APPS:
    (r'^attachments/', include('attachments.urls')),



#urlpatterns += patterns('core.memcached_status',
#    url(r'^status/cache/$', 'view'),
#)

urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^assets/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )
