from django.core.management.base import BaseCommand
import datetime
#import time
from attachments.models import Attachment
from attachments.util import get_youtube_video_id, is_valid_youtube_video

import logging
log = logging.getLogger(__name__)

class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        run_time = datetime.datetime.now()
        #cutoff = run_time - datetime.timedelta(Attachment.ATTACHMENT_VALIDITY_CHECK_INTERVAL)
        #exception_count = 0
        #while exception_count < 3:
        videos = Attachment.objects.filter(is_valid=False, att_type=Attachment.ATTACHMENT_TYPE_VIDEO)
        log.debug('verifying %s attachment' % videos.count())
        for video in videos:
            if video.url.strip() != '': # and video.last_validity_check < cutoff:
                video_id = None
                try:
                    video_id = get_youtube_video_id(video.url)
                except ValueError, e:
                    log.error("%s. for url: %s. attachment id: %s" % (e, video.url, video.pk))
                    #exception_count+=1
                except Exception, e:
                    log.error("Got exception while running verifying attachment: %s. for url: %s. attachment id: %s" % (e, video.url, video.pk))
                if video_id:
                    video.is_valid = is_valid_youtube_video(video_id)
                    video.save()
                    log.debug("verified %s to be a valid youtube url" % video.url)
        #time.sleep(Attachment.ATTACHMENT_VALIDITY_CHECK_INTERVAL)
