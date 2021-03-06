from django.shortcuts import redirect, get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from web.core.views import LoginRequiredMixin
from web.accounts.mixins import PlayerMissionStateContextMixin, MissionContextMixin
from ..models import *
from ..forms import MultiResponseForm
from ..mixins import ChallengeContextMixin

import logging
log = logging.getLogger(__name__)


class MultiResponseDetailView(LoginRequiredMixin, 
                              PlayerMissionStateContextMixin,
                              MissionContextMixin,
                              ChallengeContextMixin,
                              DetailView, 
                              ):
    model = MultiResponseChallenge
    template_name = 'challenges/multi_overview.html'
    pk_url_kwarg = 'challenge_id'
    context_object_name = 'challenge'

    def dispatch(self, request, *args, **kwargs):
        self.challenge = get_object_or_404(Challenge, pk=kwargs['challenge_id'])

        # make sure the challenge has not been played yet and is not
        # expired
        if not self.challenge.parent.is_expired and not \
                ChallengeAnswerWithMultipleChoices.objects.filter(
                                user=request.user, 
                                challenge=self.challenge
                ).exists():
            return redirect(self.challenge.play_url)
        return super(MultiResponseDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        ctx = super(MultiResponseDetailView, self).\
                get_context_data(mission=self.challenge.parent, *args, **kwargs)
        my_answers = ChallengeAnswerWithMultipleChoices.objects.get(
                                user=self.request.user,
                                challenge=self.object
        )
        ctx.update({
            'my_answers': my_answers,
        })
        return ctx

multi_response_detail_view = MultiResponseDetailView.as_view()



class MultiResponseCreateView(LoginRequiredMixin, 
                               PlayerMissionStateContextMixin,
                               MissionContextMixin,
                               ChallengeContextMixin,
                               CreateView, 
                               ):
    form_class = MultiResponseForm
    context_object_name = 'multi_response_answer'
    template_name = "challenges/multi.html"

    def dispatch(self, request, *args, **kwargs):
        self.challenge = get_object_or_404(MultiResponseChallenge, pk=kwargs['challenge_id'])

        if ChallengeAnswerWithMultipleChoices.objects.\
                        filter(user=request.user, challenge=self.challenge).\
                        exists():
            return redirect(self.challenge.overview_url)

        self.initial.update({'challenge': self.challenge,})
        return super(MultiResponseCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.challenge = self.challenge
        self.object.save()
        form.save_m2m()
        return redirect(self.challenge.overview_url)

    def form_invalid(self, form):
        print form.errors
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, *args, **kwargs):
        context_data = super(MultiResponseCreateView, self).\
                get_context_data(mission=self.challenge.parent, *args, **kwargs)
        context_data.update({
            'challenge': self.challenge,
        })
        return context_data

multi_response_play_view = MultiResponseCreateView.as_view()
