from stream import utils as stream_utils
from django.contrib.auth.models import User
#from web.player_activities.models import 
from web.accounts.models import UserProfilePerInstance
from web.missions.models import Mission
from web.instances.models import Instance
from .models import Badge, BadgePerPlayer

import logging
log = logging.getLogger(__name__)

def assign_challenge_completed_badges(user_id, mission_id, run_for_expired_missions=False):
    log.debug("assign badge for user %s, mission %s" %(user_id, mission_id))
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return

    try:
        mission = Mission.objects.get(pk=mission_id)
    except Mission.DoesNotExist:
        log.debug('cant locate mission %s' % mission_id)
        return

    if not user.is_active: 
        return

    if run_for_expired_missions == False and mission.is_expired():
        return

    user_prof_per_instance = UserProfilePerInstance.objects.get(instance=mission.instance, user_profile__user__pk=user_id)
    for_mission_count = len(Mission.objects.activities_for_mission(mission.slug))
    my_completed_count = len(user_prof_per_instance.my_completed_by_mission(mission))

    log.debug("completed %s out of %s challenges" % (my_completed_count, for_mission_count))
    if for_mission_count == my_completed_count:

        try:
            visionary_badge = Badge.objects.get(type=Badge.BADGE_VISIONARY)
        except Badge.DoesNotExist:
            return

        my_badge, created = BadgePerPlayer.objects.get_or_create(user=user, badge=visionary_badge)
        if created == False:
            my_badge.increment_level()
            my_badge.save()
            log.debug("incremented level for a Visionary badge for %s" % (user.get_profile().screen_name))
        else:
            log.debug("create a Visionary badge for %s" % (user.get_profile().screen_name))
        message = "Congratulations! You earned the %s badge." %( visionary_badge.title )
        user.notifications.create(content_object=user_prof_per_instance, message=message)
        stream_utils.action.send(
                user, 'badge_received', 
                action_object=mission,
                target=mission.instance,
                description='received a Visionary badge',

        )

def assign_badges_for_past_missions():
    # user this util method to assign badges for past missions
    for game in Instance.objects.current():
        past_missions = Mission.objects.past(game)
        log.debug("assigning for game %s" % game)
        for user_prof_per_instance in UserProfilePerInstance.objects.\
                                                filter(instance=game):
            for mission in past_missions:
                assign_challenge_completed_badges(
                                        str(user_prof_per_instance.get_user().pk),
                                        str(mission.pk),
                                        run_for_expired_missions=True,
                )

