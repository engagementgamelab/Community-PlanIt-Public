from django.contrib import admin
from web.attachment_types.models import VideoAttachmentInlines, AttachmentWithThumbnailInlines

from web.comments.models import *


class CommentAdmin(admin.ModelAdmin):
    list_filter = ('posted_date', 'flagged', 'hidden')
    list_display = ('posted_date', 'subject', 'user_name', 'flagged', 'hidden') # could not be used with nani:, 'message')

    actions = ['hide_selected', 'reveal_selected']
    inlines = [VideoAttachmentInlines, AttachmentWithThumbnailInlines]

    def get_actions(self, request):
        actions = super(CommentAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions
    
    def hide_selected(self, request, queryset):
        queryset.update(hidden=True)
        count = queryset.count()
        self.message_user(request, "Hid %d comment%s." % (count, (count == 1 and '' or 's')))

    def reveal_selected(self, request, queryset):
        queryset.update(hidden=False)
        count = queryset.count()
        self.message_user(request, "Revealed %d comment%s." % (count, (count == 1 and '' or 's')))

    def save_model(self, request, obj, form, change):
        super(CommentAdmin, self).save_model(request, obj, form, change)
        obj.user = request.user
        obj.save()
        request.user.get_profile().comments.add(obj)
        request.user.get_profile().save()        

    def subject(self, obj):
        return '%s: %s' % (obj.content_type, obj.content_object)

    def user_name(self, obj):
        return obj.user.get_profile() and obj.user.get_profile().screen_name or user.username

admin.site.register(Comment, CommentAdmin)
