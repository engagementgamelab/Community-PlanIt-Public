import httplib
import re

# we accept the long URLs shown in the location bar or the short versions
# produced by the Share button
YOUTUBE_URL_RE = re.compile(r'^https?://(?:www.youtube.com/watch\?v=|youtu.be/)(?P<video_id>\w+).*$')
YOUTUBE_EMBED_CODE_RE = re.compile(r'<iframe.*src="http://www.youtube.com/embed/(?P<video_id>\w+)".*$')

def get_youtube_video_id(value):
    valid_url = YOUTUBE_URL_RE.search(value)
    if valid_url:
        return valid_url.groupdict()['video_id']

    valid_embed_code = YOUTUBE_EMBED_CODE_RE.search(value)
    if valid_embed_code:
        return valid_embed_code.groupdict()['video_id']

    return None

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
