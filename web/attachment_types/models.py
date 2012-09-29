from attachments import models as attachment_models 

from django.contrib.contenttypes import generic
from django.db import models
from django.utils.translation import ugettext as _


class Attachment(attachment_models.Attachment):

    class Meta:
        proxy = True
        verbose_name = "Document Attachment"
        verbose_name_plural = "Document Attachments"

    def __unicode__(self):
        return '%s' % (self.attachment_file.name)


class AttachmentWithThumbnail(Attachment):

    title = models.CharField(max_length=255, blank=True, default='')
    thumbnail = models.FileField(help_text="Thumb 164x100", upload_to=Attachment.attachment_upload, blank=True, null=True)

    def __unicode__(self):
        return "%s. Image Resource." % (self.title,)


class AttachmentVideo(Attachment):

    title = models.CharField(max_length=255, blank=True, default='')
    url = models.URLField(verbose_name='Youtube.com or Vimeo.com video')

    # we try to validate URLs, but it's expensive -- you don't want to 
    # check every comment attachment when loading a page with a discussion --
    # so we cache the results of each check and update attachment status with a
    # task run under supervisor
    is_valid = models.BooleanField(default=False, editable=False)

    def __unicode__(self):
        return "%s at <%s>" % (self.title, self.url)


class AttachmentHyperlink(Attachment):

    title = models.CharField(max_length=255, blank=True, default='')
    url = models.URLField(verbose_name='Hyperlink Resource')

    def __unicode__(self):
        return "%s at <%s>" % (self.title, self.url)
