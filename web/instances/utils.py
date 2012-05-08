from operator import itemgetter 
from cache_utils.decorators import cached

from web.accounts.models import UserProfilePerInstance

import logging
log = logging.getLogger(__name__)

def leaderboard(profiles_for_game, exclude_zero_points=True):
    for_game = []
    for prof_per_instance in profiles_for_game:
        points = UserProfilePerInstance.objects.total_points_for_profile(prof_per_instance.instance, prof_per_instance.user_profile)
        #points = profile.total_points
        if not (exclude_zero_points is True and points == 0):
            for_game.append((prof_per_instance, prof_per_instance.user_profile.screen_name, points))
    return sorted(for_game, key=itemgetter(2,1), reverse=True)

@cached(60*60*24)
def leaderboard_for_game(game):
    # rank
    # screen_name
    # url to profile
    log.debug("getting the leaderboard for %s. ** not cached **" % game)
    profiles_for_game = UserProfilePerInstance.objects.filter(instance=game).\
                                                    exclude(user_profile__user__is_active=False)
    return leaderboard(profiles_for_game)


