import httplib
import re

from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

import logging
log = logging.getLogger(__name__)

# we accept the long URLs shown in the location bar or the short versions
# produced by the Share button
YOUTUBE_URL_RE = re.compile(r'^https?://(?:www.youtube.com/watch\?v=|youtu.be/)(?P<video_id>[-\w]{11}).*$')
YOUTUBE_EMBED_CODE_RE = re.compile(r'<iframe.*src="https://www.youtube.com/embed/(?P<video_id>[-\w]{11})".*$')
YOUTUBE_EMBEDDING_TEMPLATE = (
    '<iframe '
    'class="youtube-player" '
    'type="text/html" '
    'width="100%%" '
    'height="100%%" '
    'src="http://www.youtube.com/embed/%s" '
    'frameborder="0">'
    '</iframe>'
)

VIMEO_URL_RE = re.compile(r'^https?://(?:(?:player|www)\.)?vimeo.com/(?:video/)?(?P<video_id>\d+)/?$')
VIMEO_EMBED_CODE_RE = re.compile(r'<iframe.*src="https://player.vimeo.com/video/(?P<video_id>\d+)".*$')
VIMEO_EMBEDDING_TEMPLATE = (
    '<iframe '
    'src="http://player.vimeo.com/video/%s?title=0&amp;byline=0&amp;portrait=0" '
    'width="100%%" '
    'height="100%%" '
    'frameborder="0" '
    'webkitAllowFullScreen '
    'allowFullScreen>'
    '</iframe>'
)

def get_video_embedding_code(url):
    """
    Returns valid code to embed a Vimeo or YouTube video, or a placeholder.
    """
    output = mark_safe('<div class="notice">%s</div>' % unicode(_('This video is currently unavailable.')))

    video_id = None
    try:
        video_id = get_vimeo_video_id(url)
        output = VIMEO_EMBEDDING_TEMPLATE % video_id
    except ValueError:
        log.debug("NOT VIMEO URL: %s" % url)
        try:
            video_id = get_youtube_video_id(url)
            output = YOUTUBE_EMBEDDING_TEMPLATE % video_id
        except ValueError:
            pass

    return output

def get_vimeo_video_id(value):
    valid_url = VIMEO_URL_RE.search(value)
    if valid_url:
        return valid_url.groupdict()['video_id']

    valid_embed_code = VIMEO_EMBED_CODE_RE.search(value)
    if valid_embed_code:
        return valid_embed_code.groupdict()['video_id']

    raise ValueError('Supplied URL is not valid Vimeo embedding code, or the video ID is incorrect.')

def get_youtube_video_id(value):
    valid_url = YOUTUBE_URL_RE.search(value)
    if valid_url:
        return valid_url.groupdict()['video_id']

    valid_embed_code = YOUTUBE_EMBED_CODE_RE.search(value)
    if valid_embed_code:
        return valid_embed_code.groupdict()['video_id']

    raise ValueError('Supplied URL is not valid YouTube embedding code, or the video ID is incorrect.')

def is_valid_youtube_video(video_id):
    """
    Try to verify that a given URL actually points to a valid video on YouTube.
    """
    c = httplib.HTTPConnection('gdata.youtube.com')
    c.request('HEAD', '/feeds/api/videos/' + video_id)
    r = c.getresponse()
    if r.status == 200:
        return True
    return False
