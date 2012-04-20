import datetime

from django.db import models

from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _


from web.instances.models import Instance

def determine_path(instance, filename):
    return 'uploads/'+ str(instance.user.id) +'/'+ 'thumb_'+filename

ATTACHMENT_VALIDITY_CHECK_INTERVAL = 3600

        
class Attachment(models.Model):

    ATTACHMENT_TYPE_PICTURE, ATTACHMENT_TYPE_VIDEO, ATTACHMENT_TYPE_IMAGE, \
    ATTACHMENT_TYPE_CHART, ATTACHMENT_TYPE_GRAPH, \
    ATTACHMENT_TYPE_HYPERLINK, ATTACHMENT_TYPE_DOCUMENT = xrange(1,8)

    ATTACHMENT_TYPES =(
        (ATTACHMENT_TYPE_PICTURE, _("Picture")),
        (ATTACHMENT_TYPE_VIDEO, _("Video")),
        (ATTACHMENT_TYPE_IMAGE, _("Image")),
        (ATTACHMENT_TYPE_CHART, _("Chart")),
        (ATTACHMENT_TYPE_GRAPH, _("Graph")),
        (ATTACHMENT_TYPE_HYPERLINK, _("Hyperlink")),
        (ATTACHMENT_TYPE_DOCUMENT, _("Document")),
    )

    title = models.CharField(max_length=255, blank=True, default='')
    file = models.FileField(upload_to=determine_path, blank=True, null=True)
    thumbnail = models.FileField(help_text="Thumb 164x100", upload_to=determine_path, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    att_type = models.IntegerField("Attachment Type", choices=ATTACHMENT_TYPES, blank=True, null=True)
    flagged = models.IntegerField(default=0)
    user = models.ForeignKey(User, blank=True, null=True, editable=False)
    instance = models.ForeignKey(Instance, blank=True, null=True)

    is_slideshow = models.BooleanField(verbose_name=_("Display as part of a Slideshow"), default=False)
    is_resource_center = models.BooleanField(verbose_name=_("Display as part of the Resource Center"), default=False)

    # we try to validate URLs, but it's expensive -- you don't want to 
    # check every comment attachment when loading a page with a discussion --
    # so we cache the results of each check and update attachment status with a
    # task run under supervisor
    is_valid = models.BooleanField(default=False, editable=False)
    last_validity_check = models.DateTimeField(default=datetime.datetime.now, editable=False)

    @property 
    def resource_type(self):
        l = {
            Attachment.ATTACHMENT_TYPE_VIDEO : 'video',
            Attachment.ATTACHMENT_TYPE_HYPERLINK : 'link',
            Attachment.ATTACHMENT_TYPE_PICTURE : 'image',
            Attachment.ATTACHMENT_TYPE_IMAGE : 'image',
            Attachment.ATTACHMENT_TYPE_DOCUMENT  : 'document',
            Attachment.ATTACHMENT_TYPE_CHART : 'document',
            Attachment.ATTACHMENT_TYPE_GRAPH : 'document',
        }

        return l.get(self.att_type)
    
    def __unicode__(self):
        if self.url:
          return self.url[:25] or "None"
          
        if self.file:
          return self.file.url[:25]
          
        return 'None'
