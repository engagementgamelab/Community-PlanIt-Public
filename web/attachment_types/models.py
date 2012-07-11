from attachments.models import Attachment

from django.contrib.contenttypes import generic
from django.db import models
from django.utils.translation import ugettext as _


class AttachmentWithThumbnail(Attachment):

    title = models.CharField(max_length=255, blank=True, default='')
    thumbnail = models.FileField(help_text="Thumb 164x100", upload_to=Attachment.attachment_upload, blank=True, null=True)


class AttachmentWithThumbnailInlines(generic.GenericStackedInline):
    model = AttachmentWithThumbnail
    extra = 1


class AttachmentVideo(Attachment):

    title = models.CharField(max_length=255, blank=True, default='')
    url = models.CharField(max_length=255, blank=True, null=True)
    # we try to validate URLs, but it's expensive -- you don't want to 
    # check every comment attachment when loading a page with a discussion --
    # so we cache the results of each check and update attachment status with a
    # task run under supervisor
    is_valid = models.BooleanField(default=False, editable=False)


class VideoAttachmentInlines(generic.GenericStackedInline):
    model = AttachmentVideo
    extra = 1
