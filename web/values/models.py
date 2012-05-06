from stream import utils as stream_utils
from nani.models import TranslatableModel, TranslatedFields
from nani.manager import TranslationManager

from cache_utils.decorators import cached

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic

from web.instances.models import Instance
from web.comments.models import Comment

class ValueManager(TranslationManager):
    pass


#Make the comments into a foreign key field. There is no reason why
# a comment should belong to more than 1 value
class Value(TranslatableModel):

    instance = models.ForeignKey(Instance, related_name='values')
    comments = generic.GenericRelation(Comment)

    translations = TranslatedFields(
        message = models.CharField(max_length=60, verbose_name='Name'),
        description = models.TextField(max_length=1000, verbose_name='Description', default=''),
    )
    objects = ValueManager()

    @property
    def stream_action_title(self):
        return str(self.message)

    def __unicode__(self):
        return self.safe_translation_getter('message', '%s' % self.pk)

    @models.permalink
    def get_absolute_url(self):
        return ('values:detail', [str(self.id)])

stream_utils.register_target(Value)
stream_utils.register_action_object(Value)

class PlayerValueManager(models.Manager):

    @cached(60*60*24)
    def for_instance(self, instance):
        return self.filter(value__instance=instance)

    def total_flags_by_game(self, instance, value):
        return PlayerValue.objects.for_instance(instance=instance).filter(value=value).aggregate(models.Sum('coins')).get('coins__sum') or 0

    @cached(60*60*24, 'my_spent_flags')
    def total_flags_for_player(self, instance, user, value=None):
        player_values = self.for_instance(instance=instance).filter(user=user)
        if value is not None:
            player_values = player_values.filter(value=value)
        return player_values.aggregate(models.Sum('coins')).get('coins__sum') or 0

class PlayerValue(models.Model):

    user = models.ForeignKey(User)
    value = models.ForeignKey(Value)
    coins = models.IntegerField(default=0)

    objects = PlayerValueManager()

    class Meta:
        unique_together = (('user', 'value'),)

    def __unicode__(self):
        return "%s for user <%s>" % (self.value.message, self.user)


