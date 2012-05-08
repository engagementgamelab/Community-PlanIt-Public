from cache_utils.decorators import cached

from django.db import models

from accounts.models import UserProfilePerInstance
from instances.models import Instance, Affiliation

# Create your models here.


class PlayerLeaderboardManager(models.Manager):

    #@cached(60*60*24)
    def for_game(self, game):
        return self.filter(player__instance=game).exclude(points=0).order_by('-points')

class PlayerLeaderboard(models.Model):
    player = models.ForeignKey(UserProfilePerInstance, unique=True, related_name="player_leaderboard_entries" )
    screen_name = models.CharField(max_length="100", default='')
    absolute_url = models.CharField(max_length="100", default='')
    points = models.IntegerField(default=0)
    rank = models.IntegerField(default=0, null=True)
    date_last_built = models.DateTimeField(null=True)

    objects = PlayerLeaderboardManager()


class AffiliationLeaderboardManager(models.Manager):

    #@cached(60*60*24)
    def for_game(self, game):
        return self.filter(instance=game).exclude(points=0).order_by('-points')


class AffiliationLeaderboard(models.Model):
    instance = models.ForeignKey(Instance)
    affiliation = models.ForeignKey(Affiliation, related_name="affiliation_leaderboard_entries")
    name = models.CharField(max_length="100", default='')
    absolute_url = models.CharField(max_length="100", default='')
    points = models.IntegerField(default=0)
    rank = models.IntegerField(default=0, null=True)

    date_last_built = models.DateTimeField(null=True)

    objects = AffiliationLeaderboardManager()

    class Meta:
        unique_together = ('instance', 'affiliation')
