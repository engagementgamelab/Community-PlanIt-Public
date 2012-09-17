from web.accounts.models import UserProfilePerInstance, PlayerMissionState
from web.challenges.models import Challenge


class PlayerMissionStateContextMixin(object):
    """ on ChallengeListView create and initialize PlayerMissionState """

    def get_context_data(self, *args, **kwargs):
        ctx = super(PlayerMissionStateContextMixin, self).get_context_data(*args, **kwargs)
        mission = kwargs.get('mission')
        if mission is None:
            raise RuntimeError("Cannot retrieve player mission context. Mission missing from context.")
        try:
            profile_per_instance = UserProfilePerInstance.objects.get(
                                        user_profile=self.request.user.get_profile(),
                                        instance=mission.parent,
            )
            game_profile_exists = True
        except UserProfilePerInstance.DoesNotExist:
            game_profile_exists = False

        player_mission_state, created = PlayerMissionState.objects.get_or_create(
                profile_per_instance=profile_per_instance,
                mission=mission,
        )
        if created:
            player_mission_state.init_state()

        ctx['player_mission_state'] = player_mission_state
        ctx['profile_per_instance'] = profile_per_instance 

        return ctx

class MissionContextMixin(object):
    """ Context for missions and challenges """

    def get_context_data(self, *args, **kwargs):
        context = super(MissionContextMixin, self).get_context_data(*args, **kwargs)

        active_game = self.request.session.get('my_active_game', None)

        if 'mission' in kwargs:
            mission = kwargs.get('mission')
        else:
            mission = active_game.active_mission

        context['mission'] = mission.get_real_instance()
        context['active_game'] = active_game
        context['challenges'] = Challenge.objects.get_real_instances(mission.get_children())
        return context
