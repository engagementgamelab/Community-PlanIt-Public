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
            ctx['profile_per_instance'] = UserProfilePerInstance.objects.get(
                                        user_profile=up,
                                        instance=mission.game,
            )
            game_profile_exists = True
        except UserProfilePerInstance.DoesNotExist:
            game_profile_exists = False

        # retrieve or initialize mission state
        try:
            mst =  mission.mission_states.get(user=self.request.user)
        except PlayerMissionState.DoesNotExist:
            mst = PlayerMissionState.objects.create(
                    user=self.request.user,
                    mission=mission,
            )
        else:
            ctx['mst'] = mst

        return ctx

class MissionContextMixin(object):
    """ Context for missions and challenges """

    def get_context_data(self, *args, **kwargs):
        context = super(MissionContextMixin, self).get_context_data(*args, **kwargs)

        active_game = self.request.session.get('my_active_game', None)
        context['active_game'] = active_game
        context['active_mission'] = active_game.active_mission

        if 'mission' in kwargs: 
            mission = kwargs.get('mission').get_real_instance()
            context['mission'] = mission
            context['challenges'] = Challenge.objects.get_real_instances(mission.get_children())

        return context
