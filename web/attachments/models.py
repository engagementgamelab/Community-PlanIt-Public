import datetime
import magic

from django.db import models

from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from PIL import Image

from web.instances.models import Instance

def determine_path(instance, filename):
    return 'uploads/'+ str(instance.user.id) +'/'+ filename

ATTACHMENT_VALIDITY_CHECK_INTERVAL = 3600

class AttachmentSlideshowManager(models.Manager):
    def get_query_set(self):
        return super(AttachmentSlideshowManager, self).get_query_set().filter(is_slideshow=True)
        
class Attachment(models.Model):

    ATTACHMENT_TYPE_PICTURE, ATTACHMENT_TYPE_VIDEO, ATTACHMENT_TYPE_IMAGE, \
    ATTACHMENT_TYPE_CHART, ATTACHMENT_TYPE_RESOURCE_CENTER, ATTACHMENT_TYPE_GRAPH = xrange(1,7)

    ATTACHMENT_TYPES =[
        (ATTACHMENT_TYPE_PICTURE, _("Picture")),
        (ATTACHMENT_TYPE_VIDEO, _("Video")),
        (ATTACHMENT_TYPE_IMAGE, _("Image")),
        (ATTACHMENT_TYPE_CHART, _("Chart")),
        (ATTACHMENT_TYPE_GRAPH, _("Graph")),
        (ATTACHMENT_TYPE_RESOURCE_CENTER, _("Resource Center")),
    ]

    file = models.FileField(upload_to=determine_path, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True, editable=False)
    att_type = models.IntegerField("Attachment Type", choices=ATTACHMENT_TYPES, blank=True, null=True)
    flagged = models.IntegerField(default=0)
    user = models.ForeignKey(User, blank=True, null=True, editable=False)
    instance = models.ForeignKey(Instance, blank=True, null=True)

    is_slideshow = models.BooleanField(verbose_name=_("Display as part of a Slideshow"), default=False)

    slideshow = AttachmentSlideshowManager()

    # we try to validate URLs, but it's expensive -- you don't want to 
    # check every comment attachment when loading a page with a discussion --
    # so we cache the results of each check and update attachment status with a
    # task run under supervisor
    is_valid = models.BooleanField(default=True)
    last_validity_check = models.DateTimeField(default=datetime.datetime.now)

    def __unicode__(self):
        if self.url:
          return self.url[:25] or "None"
          
        if self.file:
          return self.file.url[:25]
          
        return 'None'
