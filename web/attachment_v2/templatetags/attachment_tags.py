import re

from django.conf import settings
from django import http
from django import template
from django.utils.html import fix_ampersands
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from attachments.util import get_video_embedding_code

register = template.Library()

class EmbedVideoNode(template.Node):
    """
    Renders safe video embedding code for video IDs extracted from
    user-supplied URLs or embedding code.
    """
    def __init__(self, url):
        self.url = url

    def render(self, context):
        url = template.Variable(self.url).resolve(context)
        return get_video_embedding_code(url)

@register.tag
def embed_video(parser, argument_string):
    argv = argument_string.split_contents()
    argc = len(argv)
    if argc == 2:
        return EmbedVideoNode(argv[1])
    
    raise template.TemplateSyntaxError("The %s tag requires a video URL." % argv[0])
