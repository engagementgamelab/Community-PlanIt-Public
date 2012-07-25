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
from web.core.views import LoginRequiredMixin

import logging
log = logging.getLogger(__name__)


class MissionDetail(LoginRequiredMixin, DetailView):
    model = Mission
    template_name = 'missions/mission.html'
    #queryset = Instance.objects.exclude(is_disabled=True)
    pk_url_kwarg = 'mission_id'

    def get_context_data(self, **kwargs):
        context = super(MissionDetail, self).get_context_data(
            **kwargs)
        mission = kwargs['object']
        game = mission.instance

        #if settings.DEBUG == True:
        #    if self.request.user.is_authenticated():
        #        my_profiles = UserProfilePerInstance.objects.filter(
        #                user_profile__user=self.request.user
        #        )
        #        my_profile = self.request.user.get_profile()
        #        context['my_games'] = ['I am signed up for: ']+[prof.instance.title for prof in my_profiles]
        #        context['my_profile_data'] = "".join([my_profile.screen_name, "<", self.request.user.email, '>'])

        return context

mission_detail_view = MissionDetail.as_view()


class MissionDetailPlayerCreated(MissionDetail):
    pass

mission_detail_player_created_view = MissionDetailPlayerCreated.as_view()


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

mission_detail_with_demographic_form_view = MissionDetailWithDemographicForm.as_view()
