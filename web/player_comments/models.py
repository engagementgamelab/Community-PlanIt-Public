from django.db import models
from django.contrib.auth.models import User
from django.contrib.comments.models import Comment
from django.contrib.comments.managers import CommentManager
from django.utils.translation import ugettext_lazy as _


class PlayerCommentManager(CommentManager):
    pass


class PlayerComment(Comment):
    hidden = models.BooleanField(default=False)

    # Manager
    objects = PlayerCommentManager()


class PlayerCommentLike(models.Model):
    """ Records a like on a comment.  """

    user = models.ForeignKey(User, verbose_name=_('user'), related_name="comment_likes")
    comment = models.ForeignKey(PlayerComment, verbose_name=_('comment'), related_name="likes")
    like_date = models.DateTimeField(_('date'), default=None)

    class Meta:
        unique_together = [('user', 'comment')]
        verbose_name = _('comment like')
        verbose_name_plural = _('comment likes')

    def __unicode__(self):
        return "like of comment ID %s by %s" % \
            (self.comment_id, self.user.username)

    def save(self, *args, **kwargs):
        if self.like_date is None:
            self.like_date = timezone.now()
        super(PlayerCommentLike, self).save(*args, **kwargs)
