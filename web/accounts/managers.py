from django.db import models
from cache_utils.decorators import cached

import logging
log = logging.getLogger(__name__)


class UserProfilePerInstanceManager(models.Manager):


    #@cached(60*60*24, 'user_profile_per_instance_get')
    #def get(self, *args, **kwargs):
    #    return super(UserProfilePerInstanceManager, self).get(*args, **kwargs)

    @cached(60*60*24, 'all_games_for_profile')
    def games_for_profile(self, user_profile):
        game_pks = self.filter(user_profile=user_profile).values_list('instance__pk', flat=True)
        my_games = Instance.objects.filter(pk__in=game_pks)
        return my_games

    # deprecated. points now come from the core.PlayerLeaderboard
    #@cached(60*60*24)
    #def total_points_for_profile(self, instance, user_profile):
    #    log.debug("profile manager: total_points_for_profile %s ** not cached **" % user_profile.screen_name)
    #    try:
    #        return self.get(instance=instance, user_profile=user_profile).total_points
    #    except UserProfilePerInstance.DoesNotExist:
    #        return 0

    #@cached(60*60*24, 'progress_data_for_mission')
    def progress_data_for_mission(self, instance, mission, user_profile):
        return self.get(instance=instance, user_profile=user_profile).\
                progress_percentage_by_mission(mission)

    #def latest_instance_by_profile(self, user_profile, domain):
    #    return self.objects.filter(user_profile=user_profile).latest_for_city_domain(domain)

    #def total_points_by_affiliation(self, instance, affiliation_slug):
    #    total_points = 0
    #    for player_profile in self.all_by_affiliation(instance, affiliation_slug):
    #        total_points+=self.total_points_for_profile(instance, player_profile)
    #    return total_points


class PlayerMissionStateManager(models.Manager):

    def by_game(self, game, user):
        """ return player mission states by game """
        return self.filter(mission__parent=game, user=user)

    def by_completed_mission(self, game, user):
        """ return player mission states for completed missions """
        return [ms for ms in self.by_game(game, user) if ms.is_mission_completed]

    def coins_for_completed_missions(self, game, user):
        coins = 0
        for ms in self.by_completed_mission(game, user):
            coins += ms.coins
        return coins

    def create(self, *args, **kwargs):
        if 'user' in kwargs:
            log.debug("init ms for user %s" % kwargs.get('user'))

        mission = kwargs.get('mission')
        obj = super(PlayerMissionStateManager, self).create(*args, **kwargs)
        sorted_challenges = mission.challenges_as_sorteddict
        #import pprint
        #pp = pprint.PrettyPrinter(indent=4)
        #pp.pprint(dict(sorted_challenges))
        for i, barrier in enumerate(sorted_challenges):
            if i == 0:
                obj.unlocked.add(barrier)
                for challenge in sorted_challenges.get(barrier):
                    obj.unlocked.add(challenge)
                    log.debug('adding to unlocked %s' % challenge)
            else:
                obj.locked.add(barrier)
                for challenge in sorted_challenges.get(barrier):
                    obj.locked.add(challenge)
                    log.debug('adding to locked %s' % challenge)
        return obj






