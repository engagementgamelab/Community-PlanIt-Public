from web.accounts.models import UserProfilePerInstance, PlayerMissionState
from web.challenges.models import Challenge


class PlayerMissionStateContextMixin(object):
    """ on ChallengeListView create and initialize PlayerMissionState 
        note: define after Create/DetailView as this mixin expects the mission
        to be set in the context data.  """

    def get_context_data(self, *args, **kwargs):
        ctx = super(PlayerMissionStateContextMixin, self).\
                get_context_data(*args, **kwargs)
        obj = ctx.get('object')
        mission = None
        if obj and isinstance(obj, Challenge):
            mission = obj.parent
        else:
            mission = ctx.get('mission')

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

