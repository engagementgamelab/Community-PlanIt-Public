import magic
from django.contrib.auth.models import User
from web.instances.models import Instance

from django.contrib import admin
from django.db import models

def determine_path(instance, filename):
    return 'uploads/'+ str(instance.user.id) +'/'+ filename

class Attachment(models.Model):
    file = models.FileField(upload_to=determine_path, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True, editable=False)
    type = models.CharField(max_length=45, blank=True, editable=False)
    flagged = models.IntegerField(default=0)
    user = models.ForeignKey(User, blank=True, null=True, editable=False)
    instance = models.ForeignKey(Instance, blank=True, null=True, editable=False)

    def __unicode__(self):
        if self.url:
          return self.url[:25] or "None"
          
        if self.file:
          return self.file.url[:25]
          
        return 'None'

def attachment_post_save(instance, created, **kwargs):
    if created:
        try:
            if not instance.type:
                m = magic.Magic(mime=True)
                instance.type = m.from_file(instance.file.path)
                instance.save()
        except: pass

models.signals.post_save.connect(attachment_post_save, sender=Attachment)

class AttachmentAdmin(admin.ModelAdmin):
    def queryset(self, request):
        qs = super(AttachmentAdmin, self).queryset(request)
        return qs.filter(instance=request.session.get('admin_instance'))

    def save_model(self, request, obj, form, change):
        obj.instance = request.session.get('admin_instance')
        obj.user = request.user
        obj.save()
