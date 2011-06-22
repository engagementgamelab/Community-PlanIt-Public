from web.instances.models import Instance
from web.attachments.models import Attachment
from django.contrib.auth.models import User

from django.db import models
from django.contrib import admin

#Change flagged to either a bitfield or change to flaggedBy and link a foreign key to a user. 
#TODO: Make foreign keys to each object that the Comment can be referenced from.
# For example Issue has a M:M relationship to Comment, add issue_id foreign key
# to here.
class Comment(models.Model):
    message = models.CharField(max_length=1000)
    posted_date = models.DateTimeField(auto_now_add=True)
    flagged = models.IntegerField(default=0)
    hidden = models.BooleanField(default=False)

    attachment = models.ManyToManyField(Attachment, blank=True, null=True)
    user = models.ForeignKey(User, editable=False)
    instance = models.ForeignKey(Instance, editable=False)
    comments = models.ManyToManyField('self', symmetrical=False, blank=True, editable=False)
    likes = models.ManyToManyField(User, blank=True, editable=False, related_name='liked_comments')

    def __unicode__(self):
        return self.message[:25] or ''

    @property
    def discussion_count(self):
        total = self.comments.count()
        for comment in self.comments.all():
            total += comment.discussion_count
        return total

class CommentAdmin(admin.ModelAdmin):
    list_filter = ('posted_date', 'flagged', 'hidden')
    list_display = ('posted_date', 'user', 'flagged', 'hidden', 'message')

    actions = ['hide_selected', 'reveal_selected']

    def get_actions(self, request):
        actions = super(CommentAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions
    
    def hide_selected(self, request, queryset):
        queryset.update(hidden=True)
        count = queryset.count()
        self.message_user(request, "Hid %d comment%s." % (count, (count == 1 and '' or 's')))

    def queryset(self, request):
        qs = super(CommentAdmin, self).queryset(request)
        return qs.filter(instance=request.session.get('admin_instance'))

    def save_model(self, request, obj, form, change):
        obj.instance = request.session.get('admin_instance')
        obj.user = request.user
        obj.save()

    def reveal_selected(self, request, queryset):
        queryset.update(hidden=False)
        count = queryset.count()
        self.message_user(request, "Revealed %d comment%s." % (count, (count == 1 and '' or 's')))

