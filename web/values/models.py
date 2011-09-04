from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic

from instances.models import Instance
from comments.models import Comment

from nani.models import TranslatableModel, TranslatedFields
from nani.manager import TranslationManager

#TODO: change coins to something like coinsSpentOnIntance or something
#more descriptive
#Make the comments into a foreign key field. There is no reason why
# a comment should belong to more than 1 value
class Value(TranslatableModel):
    coins = models.IntegerField(default=0)

    instance = models.ForeignKey(Instance)
    comments = generic.GenericRelation(Comment)

    translations = TranslatedFields(
        message = models.CharField(max_length=60, verbose_name='Name'),
    )

    def __unicode__(self):
        return self.safe_translation_getter('message', 'Value: %s' % self.pk)

    @models.permalink
    def get_absolute_url(self):
        return ('values_detail', [str(self.id)])

class PlayerValue(models.Model):

    user = models.ForeignKey(User)
    value = models.ForeignKey(Value)
    coins = models.IntegerField(default=0)

    def __unicode__(self):
        return "%s for user <%s>" % (self.value.message, self.user)


