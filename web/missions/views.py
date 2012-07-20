import datetime
from operator import attrgetter

from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView

from django.utils.translation import get_language
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.http import Http404

from .models import *
from web.core.utils import missions_bar_context
from web.accounts.models import UserProfilePerInstance
from web.accounts.forms import DemographicForm

import logging
log = logging.getLogger(__name__)


class MissionDetail(DetailView):
    model = Mission
    template_name = 'missions/mission.html'
    #queryset = Instance.objects.exclude(is_disabled=True)

    def get_context_data(self, **kwargs):
        context = super(MissionDetail, self).get_context_data(
            **kwargs)
        mission = kwargs['object']
        game = mission.instance
        context['game_profile_exists'] = UserProfilePerInstance.objects.filter(
                                            user_profile=self.request.user.get_profile(),
                                            instance=game,
                                        ).exists()
        try:
            prof_per_instance = UserProfilePerInstance.objects.get(
                                                user_profile=self.request.user.get_profile(),
                                                instance=game,
            )
        except UserProfilePerInstance.DoesNotExist:
            raise Http404("You are not registered for Game <%s>" % game.title)


        player_submitted_only = False

        # TODO: Should only return non-player-created challenges
        player_submitted = set(mission.player_submitted_activities(lang=get_language()))
        all_activities = player_submitted if player_submitted_only == True else \
                set(mission.activities(lang=get_language())) - player_submitted

        my_completed = set(prof_per_instance.my_completed_by_mission(mission, player_submitted_only))
        my_incomplete = all_activities - my_completed
        my_incomplete = sorted(my_incomplete, key=attrgetter('name'))
        my_completed = sorted(list(my_completed), key=attrgetter('name'))

        my_incomplete.extend(my_completed)
        all_activities_sorted = my_incomplete

        context.update(dict(
            activities = all_activities_sorted,
            my_completed = my_completed,
            all_player_submitted_cnt = len(player_submitted),
        ))

        #if settings.DEBUG == True:
        #    if self.request.user.is_authenticated():
        #        my_profiles = UserProfilePerInstance.objects.filter(
        #                user_profile__user=self.request.user
        #        )
        #        my_profile = self.request.user.get_profile()
        #        context['my_games'] = ['I am signed up for: ']+[prof.instance.title for prof in my_profiles]
        #        context['my_profile_data'] = "".join([my_profile.screen_name, "<", self.request.user.email, '>'])

        return context

mission_detail = MissionDetail.as_view()


class MissionDetailPlayerCreated(MissionDetail):
    pass

mission_detail_player_created = MissionDetailPlayerCreated.as_view()


class MissionDetailWithDemographicForm(MissionDetail, FormView):

    form_class = DemographicForm

    def get_context_data(self, **kwargs):
        context = super(MissionDetailWithDemographicForm, self).get_context_data(
            **kwargs)
        mission = kwargs['object']
        # the current game is being used by the DemographicForm to set
        # select variants
        self.initial['current_game'] = mission.instance

        context['show_demog_form'] = True

        context['form'] = self.get_form(self.form_class)

        return context

mission_detail_with_demographic_form = MissionDetailWithDemographicForm.as_view()
