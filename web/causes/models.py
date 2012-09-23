import os.path
from sorl.thumbnail import ImageField

#from stream import utils as stream_utils
from cache_utils.decorators import cached

from django.db import models
from django.contrib.auth.models import User

from web.instances.models import Instance

class CauseManager(models.Manager):
    pass


class Cause(models.Model):

    def determine_path(instance, filename):
        return os.path.join('uploads', 'causes', str(instance.instance.id), filename)

    facebook_group_url = models.URLField(null=True, blank=True)
    name = models.CharField(max_length=60, verbose_name='Organization Name')
    instance = models.ForeignKey(Instance, related_name='causes')
    creator = models.ForeignKey(User, related_name='causes')
    cause_type = models.CharField(max_length=1000, null=True, blank=True)
    description = models.TextField(max_length=1000, verbose_name='Description', blank=True, default='')
    image = ImageField(upload_to=determine_path, null=True, blank=True)
    date_added = models.DateField(auto_now_add=True)

    objects = CauseManager()

    #@property
    #def stream_action_title(self):
    #    return str(self.name)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return self.get_public_url()

    @models.permalink
    def get_game_url(self):
        return ('causes:detail_game', (), {'id': self.id})

    @models.permalink
    def get_public_url(self):
        return ('causes:detail_public', (), {'id': self.id})

#stream_utils.register_target(Cause)
#stream_utils.register_action_object(Cause)


class PlayerCauseManager(models.Manager):

    @cached(60*60*24)
    def for_instance(self, instance):
        return self.filter(cause__instance=instance)

    #def total_flags_by_game(self, instance, cause):
    #    return PlayerCause.objects.for_instance(instance=instance).filter(cause=cause).aggregate(models.Sum('coins')).get('coins__sum') or 0

    #@cached(60*60*24, 'my_spent_flags')
    #def total_flags_for_player(self, instance, user, cause=None):
    #    player_cause = self.for_instance(instance=instance).filter(user=user)
    #    if cause is not None:
    #        player_cause = player_cause.filter(cause=cause)
    #    return player_cause.aggregate(models.Sum('coins')).get('coins__sum') or 0


class PlayerCause(models.Model):

    user = models.ForeignKey(User)
    cause = models.ForeignKey(Cause)
    coins = models.IntegerField(default=0)

    objects = PlayerCauseManager()

    class Meta:
        unique_together = (('user', 'cause'),)

    def __unicode__(self):
        return "%s for user <%s>" % (self.cause.name, self.user)


