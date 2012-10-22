import datetime
from operator import attrgetter

from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView

from django.contrib.auth.decorators import login_required

from .models import *
from web.accounts.models import UserProfilePerInstance
from web.accounts.forms import DemographicForm
from web.accounts.mixins import PlayerMissionStateContextMixin, MissionContextMixin
from web.core.views import LoginRequiredMixin

import logging
log = logging.getLogger(__name__)


class MissionDetail(LoginRequiredMixin, 
                    PlayerMissionStateContextMixin, 
                    MissionContextMixin, 
                    DetailView):
    model = Mission
    template_name = 'missions/mission_detail.html'
    #queryset = Instance.objects.exclude(is_disabled=True)
    context_object_name = 'mission'
    pk_url_kwarg = 'mission_id'

    def get_context_data(self, **kwargs):
        context = super(MissionDetail, self).get_context_data(**kwargs)
        return context

mission_detail_view = MissionDetail.as_view()


class MissionDetailPlayerCreated(MissionDetail):
    pass

mission_detail_player_created_view = MissionDetailPlayerCreated.as_view()


class MissionDetailWithDemographicForm(MissionDetail, MissionContextMixin, FormView):

    form_class = DemographicForm

    def get_context_data(self, **kwargs):
        context = super(MissionDetailWithDemographicForm, self).get_context_data(
            **kwargs)
        mission = kwargs['object']
        # the current game is being used by the DemographicForm to set
        # select variants
        self.initial['current_game'] = mission.parent

        context['show_demog_form'] = True

        context['form'] = self.get_form(self.form_class)

        return context

mission_detail_with_demographic_form_view = MissionDetailWithDemographicForm.as_view()
