import datetime
import time

from web.attachments.models import *
from web.attachments.util import get_youtube_video_id, is_valid_youtube_video

run_time = datetime.datetime.now()
cutoff = run_time - datetime.timedelta(ATTACHMENT_VALIDITY_CHECK_INTERVAL)
exception_count = 0
while exception_count < 3:
    try:
        videos = Attachment.objects.filter(type="video")
        for video in videos:
            if video.url: # and video.last_validity_check < cutoff:
                video_id = get_youtube_video_id(video.url)
                if video_id:
                    video.is_valid = is_valid_youtube_video(video_id)
                else:
                    video.is_valid = False
                video.save()

        time.sleep(ATTACHMENT_VALIDITY_CHECK_INTERVAL)
    except Exception, e:
        print "Got exception:", e
