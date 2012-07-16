from django.core.management.base import BaseCommand, CommandError
from optparse import make_option

from web.attachments.models import Attachment
from web.attachments.util import get_youtube_video_id, is_valid_youtube_video

import logging
log = logging.getLogger(__name__)

class Command(BaseCommand):
    option_list = BaseCommand.option_list +(
            make_option('--attachment_id', '-a', action='store', dest='attachment_id', default=None, help='Attachment primary key to validate'),
    )
    help = 'validate urls for video attachment urls. Youtube and Vimeo supported'


    def handle(self, *args, **options):
        #log.debug("coll_command args: %s" % args)
        if len(args) > 1:
            raise CommandError("extra arguments supplied")

        def validate_url(video):
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

        attachment_id = options['attachment_id']
        if attachment_id:
            log.debug('validating url for video attachment: %s' % attachment_id)
            latest_att = Attachment.objects.latest('date_added')
            log.debug('last att: %s' % vars(latest_att))
            try:
                video = Attachment.objects.get(pk=int(attachment_id))
            except Attachment.DoesNotExist:
                log.debug("could not locate video to validate pk: %s" % attachment_id)
                return
            validate_url(video)
        else:
            # validate all 
            videos = Attachment.objects.filter(is_valid=False, att_type=Attachment.ATTACHMENT_TYPE_VIDEO)
            log.debug('verifying %s attachments' % videos.count())
            for video in videos:
                if video.url.strip() != '': # and video.last_validity_check < cutoff:
                    validate_url(video)
