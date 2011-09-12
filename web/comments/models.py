import datetime

from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

from attachments.models import Attachment
from instances.models import Instance

class Comment(models.Model):
    posted_date = models.DateTimeField(default=datetime.datetime.now)
    flagged = models.IntegerField(default=0)
    hidden = models.BooleanField(default=False)

    attachment = models.ManyToManyField(Attachment, blank=True, null=True)
    user = models.ForeignKey(User, editable=False)
    instance = models.ForeignKey(Instance, editable=False, related_name='comments')
    comments = generic.GenericRelation('self')
    likes = models.ManyToManyField(User, blank=True, editable=False, related_name='liked_comments')

    # the commented object can be of any model
    content_type  = models.ForeignKey(ContentType,
                                      blank=True, null=True,
                                      verbose_name=_('content type'),
                                      related_name="content_type_set_for_%(class)s"
                                     )
    object_id      = models.TextField(_('object ID'), blank=True)
    content_object = generic.GenericForeignKey()

    message = models.CharField(max_length=1000, blank=True, null=True)

    def __unicode__(self):
        if self.message:
            try:
                msg = self.message[:25]
            except:
                msg = self.message
        return msg

    #
    # URL resolution cribbed from django's contrib comments
    #
    def get_absolute_url(self, anchor_pattern="#comment-%(id)s"):
        return self.get_content_object_url() + (anchor_pattern % self.__dict__)

    @property
    def topic(self):
        """
        Climb up any parent comments to retrieve the thing people are
        commenting on.
        """
        comment = self
        while isinstance(comment.content_object, Comment):
            comment = comment.content_object
        return comment.content_object

    def get_content_object_url(self):
        """
        Return the URL where this comment may be viewed in context. If this
        comment is a reply, we have to climb the tree to the actual content
        object.
        """
        comment = self
        while isinstance(comment.content_object, Comment):
            comment = comment.content_object
        return reverse(
            'generic_redirect',
            args=(comment.content_type_id, comment.object_id)
        )

class CommentAdmin(admin.ModelAdmin):
    list_filter = ('posted_date', 'flagged', 'hidden')
    list_display = ('posted_date', 'subject', 'user_name', 'flagged', 'hidden') # could not be used with nani:, 'message')

    actions = ['hide_selected', 'reveal_selected']

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

