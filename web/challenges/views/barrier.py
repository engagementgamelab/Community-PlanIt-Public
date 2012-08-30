from django.shortcuts import redirect, get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from ..models import *
from ..forms import SingleResponseForm, BarrierFiftyFiftyForm
from ..mixins import PlayerMissionStateContextMixin
from web.core.views import LoginRequiredMixin

import logging
log = logging.getLogger(__name__)


class BarrierDetailView(LoginRequiredMixin, DetailView):
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
        return super(MultiResponseDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        ctx = super(BarrierDetailView, self).\
                get_context_data(mission=self.challenge.parent, *args, **kwargs)
        my_answer = AnswerWithOneChoice.objects.get(
                                user=self.request.user,
                                challenge=self.challenge
        )
        ctx.update({
            'my_answer': my_answer,
        })
        return ctx

barrier_detail_view = BarrierDetailView.as_view()


class RedirectToChallengeOverviewMixin(object):

    def dispatch(self, request, *args, **kwargs):

        return super(RedirectToChallengeOverviewMixin, self).dispatch(request, *args, **kwargs)


class BarrierCreateView(LoginRequiredMixin,
                        PlayerMissionStateContextMixin,
                        CreateView):
    form_class = SingleResponseForm
    context_object_name = 'barrier_answer'
    template_name = "challenges/barrier.html"

    def dispatch(self, request, *args, **kwargs):
        self.challenge = get_object_or_404(Challenge, pk=kwargs['challenge_id'])

        if AnswerWithOneChoice.objects.\
                filter( user=request.user, challenge=self.challenge).exists():
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
        })
        return context_data

barrier_play_view = BarrierCreateView.as_view()


class BarrierFiftyFiftyCreateView(LoginRequiredMixin,
                        PlayerMissionStateContextMixin,
                        CreateView):
    form_class = BarrierFiftyFiftyForm
    context_object_name = 'my_answer'
    template_name = "challenges/barrier.html"

    def dispatch(self, request, *args, **kwargs):
        self.challenge = get_object_or_404(Challenge, pk=kwargs['challenge_id'])

        if AnswerWithOneChoice.objects.\
                filter( user=request.user, challenge=self.challenge).exists():
            return redirect(self.challenge.overview_url)

        self.initial.update({'challenge': self.challenge,})
        return super(BarrierFiftyFiftyCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        cd = form.cleaned_data
        print cd
        answer = AnswerWithOneChoice()
        answer.user = self.request.user
        answer.challenge = self.challenge
        answer.save()
        return redirect(self.challenge.overview_url)

    def form_invalid(self, form):
        print form.errors
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, *args, **kwargs):
        context_data = super(BarrierFiftyFiftyCreateView, self).\
                get_context_data(mission=self.challenge.parent, *args, **kwargs)
        context_data.update({
            'challenge': self.challenge,
        })
        return context_data

barrier_fifty_fifty_view = BarrierFiftyFiftyCreateView.as_view()


