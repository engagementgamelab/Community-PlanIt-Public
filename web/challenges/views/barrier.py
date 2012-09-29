from django.shortcuts import redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from web.accounts.mixins import PlayerMissionStateContextMixin, MissionContextMixin
from web.core.views import LoginRequiredMixin
from ..models import *
from ..forms import SingleResponseForm, BarrierFiftyFiftyForm
from ..mixins import ChallengeContextMixin

from web.accounts.models import UserProfilePerInstance, PlayerMissionState

import logging
log = logging.getLogger(__name__)


class BarrierDetailView(LoginRequiredMixin, 
                        PlayerMissionStateContextMixin,
                        MissionContextMixin,
                        ChallengeContextMixin,
                        DetailView):
    model = BarrierChallenge
    template_name = 'challenges/barrier_overview.html'
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
        return super(BarrierDetailView, self).dispatch(request,
                                                        *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        ctx = super(BarrierDetailView, self).\
                get_context_data(mission=self.challenge.parent,
                                                        *args, **kwargs)
        my_answer = AnswerWithOneChoice.objects.get(
                                user=self.request.user,
                                challenge=self.challenge
        )
        ctx.update({
            'my_answer': my_answer,
            'my_answer_is_correct' : my_answer.selected in \
                                    self.challenge.answer_choices.\
                                    filter(is_barrier_correct_answer=True),
        })
        return ctx

barrier_detail_view = BarrierDetailView.as_view()


class BarrierCreateView(LoginRequiredMixin,
                        PlayerMissionStateContextMixin,
                        MissionContextMixin,
                        ChallengeContextMixin,
                        CreateView):
    form_class = SingleResponseForm
    context_object_name = 'barrier_answer'
    template_name = "challenges/barrier.html"

    def dispatch(self, request, *args, **kwargs):
        self.challenge = get_object_or_404(Challenge, pk=kwargs['challenge_id'])
        try:
            mst =  self.challenge.parent.mission_states.get(user=request.user)
        except PlayerMissionState.DoesNotExist:
            # if mission state has not been created and initialized
            # redirect the player back to the ChallengeListView to create it
            return redirect(
                    reverse('missions:challenges:challenges', args=[self.challenge.parent.pk,]))
        # TODO 
        # convert this to a redirect
        assert mst.coins >= self.challenge.minimum_coins_to_play, \
                "Mission `%s`. Player does not have enough coins to play the barrier." %  mst.mission.__unicode__()

        if AnswerWithOneChoice.objects.\
                filter(user=request.user, challenge=self.challenge).exists():
            return redirect(self.challenge.overview_url)

        self.initial.update({'challenge': self.challenge,})
        return super(BarrierCreateView, self).dispatch(request, *args, **kwargs)

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
        context_data = super(BarrierCreateView, self).\
                get_context_data(mission=self.challenge.parent, *args, **kwargs)
        context_data.update({
            'challenge': self.challenge,
            'fifty_fifty': False,
        })
        return context_data

barrier_play_view = BarrierCreateView.as_view()


class BarrierFiftyFiftyCreateView(LoginRequiredMixin,
                                  PlayerMissionStateContextMixin,
                                  MissionContextMixin,
                                  CreateView):

    form_class = BarrierFiftyFiftyForm
    context_object_name = 'my_answer'
    template_name = "challenges/barrier.html"

    def dispatch(self, request, *args, **kwargs):
        self.challenge = get_object_or_404(Challenge, pk=kwargs['challenge_id'])

        # check to prevent running the 50/50 twice
        # need to get the PlayerMissionState.barriers_fifty_fifty
        # *****

        # if player already answered this challenge, redirect to
        # challenge overview
        if AnswerWithOneChoice.objects.\
                filter(user=request.user, challenge=self.challenge).exists():
            return redirect(self.challenge.overview_url)

        self.initial.update({'challenge': self.challenge,})
        return super(BarrierFiftyFiftyCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        answer = AnswerWithOneChoice()
        answer.user = self.request.user
        answer.challenge = self.challenge
        answer.selected = AnswerChoice.objects.get(pk=int(form.cleaned_data.get('selected')))
        answer.save()
        return redirect(self.challenge.overview_url)

    def form_invalid(self, form):
        print form.errors
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, *args, **kwargs):
        ctx = super(BarrierFiftyFiftyCreateView, self).\
                get_context_data(mission=self.challenge.parent, *args, **kwargs)
        ctx.update({
            'challenge': self.challenge,
            'fifty_fifty': True,
        })
        #set the 50/50 request into player mission state
        mst = ctx.get('mst')
        mst.barriers_fifty_fifty.add(self.challenge)
        return ctx

barrier_fifty_fifty_view = BarrierFiftyFiftyCreateView.as_view()


