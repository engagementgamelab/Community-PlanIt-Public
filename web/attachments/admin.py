from web.attachments.models import *
from django.contrib import admin

class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('file', 'user', 'instance')
    list_filter = ('att_type', 'instance')

    def queryset(self, request):
        qs = super(AttachmentAdmin, self).queryset(request)
        return qs.filter(instance=request.session.get('admin_instance'))

    def save_model(self, request, obj, form, change):
        obj.instance = request.session.get('admin_instance')
        obj.user = request.user
        obj.save()

admin.site.register(Attachment, AttachmentAdmin)
