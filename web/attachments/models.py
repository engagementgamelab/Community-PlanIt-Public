from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from web.instances.models import BaseTreeNode

class Attachment(BaseTreeNode):

    def attachment_upload(instance, filename):
        """Stores the attachment in a dir by parent's primary key. most likely the Challenge """
        return 'attachments/{0}/{1}'.format(instance.parent.pk, filename)

    # used by django-polymorphic-tree for self explanatory purpose
    can_have_children = False

    creator = models.ForeignKey(User, related_name="created_attachments", verbose_name=_('creator'))
    attachment_file = models.FileField(_('attachment'), upload_to=attachment_upload)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    def __unicode__(self):
        return '%s attached %s' % (self.creator.username, self.attachment_file.name)

    class Meta:
        ordering = ['-created']
        permissions = (
            ('delete_foreign_attachments', 'Can delete foreign attachments'),
        )
        verbose_name = "Document Attachment"
        verbose_name_plural = "Document Attachments"


    @property
    def filename(self):
        return os.path.split(self.attachment_file.name)[1]


class AttachmentDocument(Attachment):
    pass


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
