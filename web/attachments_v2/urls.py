from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from web.attachments.views import *

urlpatterns = patterns('web.attachments.views',
    url(r'^post-game/$', 'post_game', name='post-game'),

    url(r'^(?P<slug>[-\w]+)/$', 'index', name='game-rc'),
    url(r'^$', 'index', kwargs={'extra_context': {'city_header': True,}}, name='index'),

    url(r'^resource/(?P<slug>[-\w]+)/(?P<attachment_id>\d+)$', 'attachment', name='game-attachment'),
    url(r'^resource/(?P<attachment_id>\d+)/$', 'attachment', kwargs={
        'extra_context': {
            'city_header': True,
        }
    }, name='attachment'),
    # templates dir is defined in settings_base.py
    # in TEMPLATE_DIRS
    url(r'^post-game/visualizations/detroit_demographic.html$', direct_to_template,
                { 'template': 'detroit_demographic.html' },
        name='detroit-247-postgame-demographics'),
    url(r'^post-game/visualizations/detroit_cloud.html$', direct_to_template,
                { 'template': 'detroit_cloud.html' },
        name='detroit-247-postgame-cloud'),
    url(r'^post-game/visualizations/noquwo_cloud.html$', direct_to_template,
                { 'template': 'noquwo_cloud.html' },
        name='noquwo-postgame-cloud'),

)
