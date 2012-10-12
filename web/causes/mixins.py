from django.db import models
from web.accounts.models import PlayerMissionState
from .models import Cause, PlayerCauseTransaction


class CausesContextMixin(object):
    """ insert coins counts into Bank context """

    def get_context_data(self, *args, **kwargs):
        ctx = super(CausesContextMixin, self).get_context_data(*args, **kwargs)

        coins_for_game_available  = PlayerMissionState.objects.\
                                    coins_for_completed_missions(self.request.user, self.game)

        transactions = PlayerCauseTransaction.objects.\
                            filter(user=self.request.user, cause__instance=self.game)

        coins_for_game_spent = transactions.\
                                    aggregate(models.Sum('coins')).get('coins__sum') or 0

        # [[Case, coins],]
        cause_points_spent = []
        for cause in self.game.causes.all():
            cause_points_spent.extend([cause, transactions.filter(cause=cause).\
                                aggregate(models.Sum('coins')).get('coins__sum') or 0])

        # to render the missions with coins spent
        # to see if mission has been completed -> PlayerMissionState.is_completed_mission
        mission_states_by_game = PlayerMissionState.objects.by_game(self.game, self.request.user)

        ctx['coins_for_game_available'] = coins_for_game_available
        ctx['coins_for_game_spent'] = coins_for_game_spent
        ctx['cause_points_spent'] = cause_points_spent
        ctx['mission_states_by_game'] = mission_states_by_game
        print ctx
        return ctx

