import datetime

from cache_utils.decorators import cached

from django.conf import settings
from django.http import Http404

from web.instances.models import Instance
from web.missions.models import Mission
from web.accounts.models import UserProfilePerInstance, UserProfileVariantsForInstance

from .models import PlayerLeaderboard, AffiliationLeaderboard


import logging
log = logging.getLogger(__name__)

def rebuild_player_leaderboard(profiles_for_game):

    for prof_per_instance in profiles_for_game:
        lb, created = PlayerLeaderboard.objects.get_or_create(player=prof_per_instance)
        #lb.points = UserProfilePerInstance.objects.total_points_for_profile(prof_per_instance.instance, prof_per_instance.user_profile)
        lb.points = prof_per_instance.total_points
        lb.screen_name = prof_per_instance.user_profile.screen_name
        lb.absolute_url = prof_per_instance.get_absolute_url()
        lb.date_last_built = datetime.datetime.now()
        lb.save()

def rebuild_affiliation_leaderboard(game, affiliations):

    for affiliation in affiliations:
        points = 0
        lb, created = AffiliationLeaderboard.objects.get_or_create(instance=game, affiliation=affiliation)
        for prof_per_instance in UserProfilePerInstance.objects.filter(instance=game, affils=affiliation).\
                exclude(user_profile__user__is_active=False):
            #points_for_player = UserProfilePerInstance.objects.total_points_for_profile(prof_per_instance.instance, prof_per_instance.user_profile)
            points_for_player = prof_per_instance.total_points
            if points_for_player == 0:
                continue
            points+=points_for_player
        lb.name = affiliation.name
        if affiliation.slug.strip() != '':
            lb.absolute_url = affiliation.get_absolute_url()
        lb.points = points
        lb.date_last_built = datetime.datetime.now()
        lb.save()


@cached(60*60*24)
def leaderboard_for_game(game_id):
    # rank
    # screen_name
    # url to profile
    game = Instance.objects.get(pk=int(game_id))
    profiles_for_game = UserProfilePerInstance.objects.filter(instance=game).\
                                        exclude(user_profile__user__is_active=False,
                                            user_profile__user__is_superuser=True,
                                            user_profile__user__is_staff=True,
                                        )
    rebuild_player_leaderboard(profiles_for_game)
    variants = UserProfileVariantsForInstance.objects.get(instance=game)
    affiliations = variants.affiliation_variants.all()
    rebuild_affiliation_leaderboard(game, affiliations)





