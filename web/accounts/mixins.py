from web.accounts.models import UserProfilePerInstance, PlayerMissionState
from web.challenges.models import Challenge


class PlayerMissionStateContextMixin(object):
    """ on ChallengeListView create and initialize PlayerMissionState """

    def get_context_data(self, *args, **kwargs):
        ctx = super(PlayerMissionStateContextMixin, self).get_context_data(*args, **kwargs)

        if 'mission' in kwargs:
            mission = kwargs.get('mission')
        else:
            active_game = self.request.session.get('my_active_game', None)
            if active_game is None:
                raise RuntimeError("Cannot retrieve active game from session.")
            mission = active_game.active_mission
            if mission is None:
                raise RuntimeError("Cannot retrieve active mission.")

        up = self.request.user.get_profile()
        try:
            my_game_profile = UserProfilePerInstance.objects.get(
                                        user_profile=up,
                                        instance=mission.parent,
            )
            game_profile_exists = True
        except UserProfilePerInstance.DoesNotExist:
            game_profile_exists = False

        try:
            mst =  mission.mission_states.get(user=self.request.user)
        except PlayerMissionState.DoesNotExist:
            mst = PlayerMissionState.objects.create(
                    user=self.request.user,
                    mission=mission,
            )

        ctx['mst'] = mst
        ctx['profile_per_instance'] = my_game_profile 

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
