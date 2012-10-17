from django.shortcuts import redirect, get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from web.missions.models import Mission
from web.core.views import LoginRequiredMixin
from ..models import *
from ..forms import SingleResponseForm
from web.accounts.mixins import PlayerMissionStateContextMixin, MissionContextMixin
from ..mixins import ChallengeContextMixin

import logging
log = logging.getLogger(__name__)


class SingleResponseDetailView(LoginRequiredMixin,
                               PlayerMissionStateContextMixin,
                               MissionContextMixin,
                               ChallengeContextMixin,
                               DetailView,
                               ):
    model = SingleResponseChallenge
    template_name = 'challenges/single_overview.html'
    pk_url_kwarg = 'challenge_id'
    context_object_name = 'challenge'

    def dispatch(self, request, *args, **kwargs):
        self.challenge = get_object_or_404(Challenge, pk=kwargs['challenge_id'])

        # make sure the challenge has not been played yet and is not
        # expired
        if not self.challenge.parent.is_expired and not \
                AnswerWithOneChoice.objects.filter(
                                user=request.user, 
                                challenge=self.challenge
                ).exists():
            return redirect(self.challenge.play_url)
        return super(SingleResponseDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        ctx = super(SingleResponseDetailView, self).\
                get_context_data(mission=self.challenge.parent, *args, **kwargs)
        my_answer = AnswerWithOneChoice.objects.get(
                                user=self.request.user,
                                challenge=self.challenge
        )
        ctx.update({
            'my_answer': my_answer,
        })
        return ctx

single_response_detail_view = SingleResponseDetailView.as_view()


class SingleResponseCreateView(LoginRequiredMixin,
                               PlayerMissionStateContextMixin,
                               MissionContextMixin,
                               ChallengeContextMixin,
                               CreateView):
    form_class = SingleResponseForm
    template_name = "challenges/single.html"

    def dispatch(self, request, *args, **kwargs):
        self.challenge = get_object_or_404(Challenge, pk=kwargs['challenge_id'])

        if AnswerWithOneChoice.objects.\
                    filter(user=request.user, challenge=self.challenge).exists():
            log.debug("%s has already been played by %s. redirecting to overview." % 
                                (self.challenge, request.user))
            return redirect(self.challenge.overview_url)

        self.initial.update({'challenge': self.challenge,})
        return super(SingleResponseCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.challenge = self.challenge
        self.object.save()
        return redirect(self.challenge.overview_url)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, *args, **kwargs):
        context_data = super(SingleResponseCreateView, self).\
                get_context_data(mission=self.challenge.parent, *args, **kwargs)
        context_data.update({
            'challenge': self.challenge,
        })
        return context_data

single_response_play_view = SingleResponseCreateView.as_view()
