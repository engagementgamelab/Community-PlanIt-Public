import re

from django.conf import settings
from django import http
from django import template
from django.utils.html import fix_ampersands
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from attachments.util import get_youtube_video_id

register = template.Library()

class YouTubeVideoNode(template.Node):
    """
    Renders safe YouTube video embedding code for video IDs extracted from
    user-supplied YouTube URLs or embedding code.
    """
    embed_iframe = (
        '<iframe '
        'class="youtube-player" '
        'type="text/html" '
        'width="100%%" '
        'height="100%%" '
        'src="http://www.youtube.com/embed/%s" '
        'frameborder="0">'
        '</iframe>'
    )
    def __init__(self, url):
        self.url = url

    def render(self, context):
        url = template.Variable(self.url).resolve(context)
        output = mark_safe('<div class="notice">%s</div>' % unicode(_('This video is currently unavailable.')))
        video_id = get_youtube_video_id(url)
        if video_id:
            output = self.embed_iframe % video_id
        return output

@register.tag
def youtube_video(parser, argument_string):
    argv = argument_string.split_contents()
    argc = len(argv)
    if argc == 2:
        return YouTubeVideoNode(argv[1])
    
    raise template.TemplateSyntaxError("The %s tag requires a video URL." % argv[0])
