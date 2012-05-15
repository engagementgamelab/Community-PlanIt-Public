from django.contrib.auth.models import User
#from web.player_activities.models import 
from web.accounts.models import UserProfilePerInstance
from web.missions.models import Mission
from .models import Badge, BadgePerPlayer

import logging
log = logging.getLogger(__name__)

def assign_challenge_completed_badges(user_id, mission_id):
    log.debug('user: %s, mission %s' % (user_id, mission_id))
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return

    try:
        mission = Mission.objects.get(pk=mission_id)
    except Mission.DoesNotExist:
        return

    if not user.is_active or mission.is_expired():
        return

    user_prof_per_instance = UserProfilePerInstance.objects.get(instance=mission.instance, user_profile__user__pk=user_id)
    for_mission_count = len(Mission.objects.activities_for_mission(mission.slug))
    my_completed_count = len(user_prof_per_instance.my_completed_by_mission(mission))

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

