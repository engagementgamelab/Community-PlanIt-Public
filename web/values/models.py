from stream import utils as stream_utils
from nani.models import TranslatableModel, TranslatedFields
from nani.manager import TranslationManager

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic

from instances.models import Instance
from comments.models import Comment

#TODO: change coins to something like coinsSpentOnIntance or something
#more descriptive
#Make the comments into a foreign key field. There is no reason why
# a comment should belong to more than 1 value
class Value(TranslatableModel):
    coins = models.IntegerField(default=0)

    instance = models.ForeignKey(Instance, related_name='values')
    comments = generic.GenericRelation(Comment)

    translations = TranslatedFields(
        message = models.CharField(max_length=60, verbose_name='Name'),
    )

    def __unicode__(self):
        return self.safe_translation_getter('message', '%s' % self.pk)

    @models.permalink
    def get_absolute_url(self):
        return ('values:detail', [str(self.id)])

stream_utils.register_target(Value)

class PlayerValue(models.Model):

    user = models.ForeignKey(User)
    value = models.ForeignKey(Value)
    coins = models.IntegerField(default=0)

    class Meta:
        unique_together = (('user', 'value'),)

    def __unicode__(self):
        return "%s for user <%s>" % (self.value.message, self.user)


