import datetime
import magic

from django.db import models

from django.contrib import admin
from django.contrib.auth.models import User

from PIL import Image

from web.instances.models import Instance

def determine_path(instance, filename):
    return 'uploads/'+ str(instance.user.id) +'/'+ filename

ATTACHMENT_VALIDITY_CHECK_INTERVAL = 3600

class Attachment(models.Model):
    file = models.FileField(upload_to=determine_path, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True, editable=False)
    type = models.CharField(max_length=45)
    flagged = models.IntegerField(default=0)
    user = models.ForeignKey(User, blank=True, null=True, editable=False)
    instance = models.ForeignKey(Instance, blank=True, null=True, editable=False)

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

    def save(self, *args, **kwargs):
        if self.type == None:
            m = magic.Magic(mime=True)
            self.type = m.from_file(instance.file.path)
        super(Attachment, self).save()

class AttachmentAdmin(admin.ModelAdmin):
    def queryset(self, request):
        qs = super(AttachmentAdmin, self).queryset(request)
        return qs.filter(instance=request.session.get('admin_instance'))

    def save_model(self, request, obj, form, change):
        obj.instance = request.session.get('admin_instance')
        obj.user = request.user
        obj.save()
