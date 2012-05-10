from PIL import Image

from web.attachments.models import Attachment

import logging
log = logging.getLogger(__name__)

def create_video_attachment(attachment_parent, video_url, game, author):

    attachment = Attachment.objects.create(
            file=None,
            url=video_url,
            att_type=Attachment.ATTACHMENT_TYPE_VIDEO,
            user=author,
            instance=game,
    )
    attachment_parent.attachment.add(attachment)
    log.debug("created attachment video url for parent %s. %s" % (attachment_parent.pk, attachment))

    try:
        # uwsgi spool
        from uwsgiutils.tasks import run_attachment_checks
        run_attachment_checks.spool(attachment_id=str(attachment.pk))
    except ImportError:
        # it is not possible to import uwsgi
        # from certain environments such as from pyshell
        # ignoring the ImportError
        pass

def create_image_attachment(attachment_parent, image_file, game, author):

    picture = Image.open(image_file)
    if (image_file.name.rfind(".") -1):
        image_file.name = "%s.%s" % (image_file.name, picture.format.lower())

    attachment = Attachment.objects.create(
        file=image_file,
        att_type=Attachment.ATTACHMENT_TYPE_IMAGE,
        is_valid=True,
        user=author,
        instance=game,
    )
    attachment_parent.attachment.add(attachment)
    log.debug("created attachment image for parent %s. %s" % (attachment_parent.pk, attachment))

