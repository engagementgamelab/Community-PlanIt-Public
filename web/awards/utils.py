#from stream import utils as stream_utils
from django.contrib.auth.models import User
#from web.player_activities.models import 
from web.accounts.models import UserProfilePerInstance
from web.missions.models import Mission
from web.instances.models import Instance
from .models import Award, PlayerAward

import logging
log = logging.getLogger(__name__)

def assign_challenge_completed_awards(user_id, mission_id, run_for_expired_missions=False):
    log.debug("assign award for user %s, mission %s" %(user_id, mission_id))
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
    for_mission_count = len(mission.activities())
    my_completed_count = len(user_prof_per_instance.my_completed_by_mission(mission))

    log.debug("completed %s out of %s challenges" % (my_completed_count, for_mission_count))
    if for_mission_count == my_completed_count:

        try:
            visionary_award = Award.objects.get(type=Award.VISIONARY)
        except Award.DoesNotExist:
            return

        my_awrd, created = PlayerAward.objects.get_or_create(user=user, award=visionary_award)
        if created == False:
            my_award.increment_level()
            my_award.save()
            log.debug("incremented level for a Visionary award for %s" % (user.get_profile().screen_name))
        else:
            log.debug("create a Visionary award for %s" % (user.get_profile().screen_name))
        message = "Congratulations! You earned the %s award." %( visionary_award.title )
        user.notifications.create(content_object=user_prof_per_instance, message=message)
        #stream_utils.action.send(
        #        user, 'award_received', 
        #        action_object=mission,
        #        target=mission.instance,
        #        description='received a Visionary award',

        )

def assign_awards_for_past_missions():
    # user this util method to assign awardsfor past missions
    for game in Instance.objects.current():
        past_missions = Mission.objects.past(game)
        log.debug("assigning for game %s" % game)
        for user_prof_per_instance in UserProfilePerInstance.objects.\
                                                filter(instance=game):
            for mission in past_missions:
                assign_challenge_completed_awards(
                                        str(user_prof_per_instance.get_user().pk),
                                        str(mission.pk),
                                        run_for_expired_missions=True,
                )

