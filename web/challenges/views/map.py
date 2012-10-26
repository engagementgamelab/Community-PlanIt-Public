from django.shortcuts import redirect, get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from web.core.views import LoginRequiredMixin
from web.accounts.mixins import PlayerMissionStateContextMixin, MissionContextMixin
from ..models import *
from ..forms import MapForm
from ..mixins import ChallengeContextMixin

import logging
log = logging.getLogger(__name__)


class MapDetailView(LoginRequiredMixin,
                    PlayerMissionStateContextMixin,
                    MissionContextMixin,
                    ChallengeContextMixin,
                    DetailView):
    model = MapChallenge
    template_name = 'challenges/map_overview.html'
    pk_url_kwarg = 'challenge_id'
    context_object_name = 'challenge'

    def dispatch(self, request, *args, **kwargs):
        self.challenge = get_object_or_404(Challenge, pk=kwargs['challenge_id'])

        # make sure the challenge has not been played yet and is not
        # expired
        if not self.challenge.parent.is_expired and not \
                ChallengeAnswerMap.objects.filter(
                                user=request.user, 
                                challenge=self.challenge
                ).exists():
            return redirect(self.challenge.play_url)
        return super(MapDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        ctx = super(MapDetailView, self).\
                get_context_data(mission=self.challenge.parent, *args, **kwargs)

        my_answer = ChallengeAnswerWithOneChoice.objects.get(
                                user=self.request.user,
                                challenge=self.challenge
        )
        ctx.update({
            'my_answer': my_answer,
        })
        return ctx

map_detail_view = MapDetailView.as_view()


class MapCreateView(LoginRequiredMixin, 
                    PlayerMissionStateContextMixin,
                    MissionContextMixin,
                    ChallengeContextMixin,
                    CreateView):
    form_class = MapForm
    template_name = "challenges/map.html"

    def dispatch(self, request, *args, **kwargs):
        self.challenge = get_object_or_404(MapChallenge, pk=kwargs['challenge_id'])

        if ChallengeAnswerMap.objects.\
                    filter(user=request.user, challenge=self.challenge).exists():
            return redirect(self.challenge.overview_url)

        self.initial.update({'challenge': self.challenge,})
        return super(MapCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.challenge = self.challenge
        self.object.save()
        return redirect(self.challenge.overview_url)

    def form_invalid(self, form):
        print form.errors
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, *args, **kwargs):
        context_data = super(MapCreateView, self).\
                get_context_data(mission=self.challenge.parent, *args, **kwargs)
        context_data.update({
            'challenge': self.challenge,
        })
        return context_data

map_play_view = MapCreateView.as_view()
