from web.accounts.models import UserProfilePerInstance, PlayerMissionState


class PlayerMissionStateContextMixin(object):

    def get_context_data(self, *args, **kwargs):
        mission = kwargs.pop('mission', None)
        ctx = super(PlayerMissionStateContextMixin, self).\
                get_context_data(*args, **kwargs)
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

