import datetime
from stream import utils as stream_utils
from cache_utils.decorators import cached
from stream.models import Action
from stream.signals import action

from django.db import models
from django.dispatch import receiver
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

from web.attachments.models import Attachment
from web.instances.models import Instance


class Comment(models.Model):
    posted_date = models.DateTimeField(default=datetime.datetime.now)
    flagged = models.IntegerField(default=0)
    hidden = models.BooleanField(default=False)

    attachment = models.ManyToManyField(Attachment, blank=True, null=True)
    user = models.ForeignKey(User, editable=False, null=True, blank=True)
    instance = models.ForeignKey(Instance, editable=False, blank=True, null=True, related_name='comments')
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

    message = models.CharField(max_length=2000, blank=True, null=True)

    @property
    def likes_users(self):
        return self.cached_likes_users(self.pk)

    @cached(60*60*24*7)
    def cached_likes_users(comment_id):
        return self.likes.values_list('pk', flat=True)

    @property
    def likes_count(self):
        return self.cached_likes_count(self.pk)

    @cached(60*60*24*7)
    def cached_likes_count(self, comment_id):
        return self.likes.all().count()

    @property
    def attachment_video_url(self):
        @cached(60*60*24*30)
        def this_attachment_video_url(comment_id):
            try:
                att = self.attachment.get(
                            att_type=Attachment.ATTACHMENT_TYPE_VIDEO
                )
            except Attachment.DoesNotExist:
                return ('', '')
            else:
                return ('invalid', att.url) if not att.is_valid else ('valid', att.url)

        return this_attachment_video_url(self.pk)

    @property
    def attachment_image_url(self):
        @cached(60*60*24*30)
        def this_attachment_image_url(comment_id):
            try:
                att = self.attachment.get(
                                att_type=Attachment.ATTACHMENT_TYPE_IMAGE,
                                file__isnull=False)
            except Attachment.DoesNotExist:
                return ''
            else:
                return att.file.url
        return this_attachment_image_url(self.pk)

    @property
    def author_screen_name(self):
        @cached(60*60*24*30)
        def this_screen_name(comment_pk):
            return self.user.get_profile().screen_name
        return this_screen_name(self.pk)

    @property
    def author_avatar(self):
        @cached(60*60*24*30)
        def this_avatar(comment_pk):
            return self.user.get_profile().avatar
        return this_avatar(self.pk)

    @property
    def author(self):
        @cached(60*60*24*30)
        def this_user(comment_pk):
            return self.user
        return this_user(self.pk)

    @property
    def is_game_active(self):
        @cached(60*60*24)
        def this_is_game_active(comment_pk):
            return self.instance.is_active()
        return this_is_game_active(self.pk)

    #@property
    #def display_user(self):
    #    return not self.is_official_response

    #@property
    #def is_official_response(self):
    #    return self.content_object.__class__.__name__ in ['PlayerActivityOfficialResponse', 'MapOfficialResponse', 'EmpathyOfficialResponse', 'ChallengeOfficialResponse']

    def __unicode__(self):
        #if self.message:
        #    return self.message
        #else:
        return str(self.pk)

    def save(self, *args, **kwargs):
        if self.message is not None and len(self.message) > 1000:
            self.message = self.message.replace('\r\n', '\n')
        super(Comment, self).save(*args, **kwargs)

    #
    # URL resolution cribbed from django's contrib comments
    #
    def get_absolute_url(self, anchor_pattern="#comment-%(id)s"):
        print self.get_content_object_url() + (anchor_pattern % self.__dict__)
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

stream_utils.register_action_object(Comment)
stream_utils.register_target(Comment)

@receiver(action, sender=Action)
def invalidate_likes_for_comment(sender, **kwargs):
    action = kwargs.pop('instance')
    if action.verb == 'liked':
        comment_id = action.target_comment.pk
        Comment.cached_likes_count.invalidate(comment_id)
        Comment.cached_likes_users.invalidate(comment_id)





