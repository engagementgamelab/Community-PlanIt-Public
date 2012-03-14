from web.attachments.models import *
from django.contrib import admin

class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('file', 'user', 'instance')
    list_filter = ('att_type', 'instance', 'is_slideshow',)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

admin.site.register(Attachment, AttachmentAdmin)
