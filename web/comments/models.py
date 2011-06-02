from web.instances.models import Instance
from web.attachments.models import Attachment
from django.contrib.auth.models import User

from django.db import models
from django.contrib import admin

class Comment(models.Model):
    message = models.CharField(max_length=1000)
    posted_date = models.DateTimeField(auto_now_add=True)
    flagged = models.IntegerField(default=0)

    attachment = models.ManyToManyField(Attachment, blank=True, null=True)
    user = models.ForeignKey(User, editable=False)
    instance = models.ForeignKey(Instance, editable=False)
    comments = models.ManyToManyField("self", symmetrical=False, blank=True, editable=False)

    def __unicode__(self):
        return self.message[:25] or ''

class CommentAdmin(admin.ModelAdmin):
    list_display = ('message', 'posted_date', 'user',)

    def queryset(self, request):
        qs = super(CommentAdmin, self).queryset(request)
        return qs.filter(instance=request.session.get('admin_instance'))

    def save_model(self, request, obj, form, change):
        obj.instance = request.session.get('admin_instance')
        obj.save()
