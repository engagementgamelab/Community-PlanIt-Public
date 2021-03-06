from django import forms
from django.utils.translation import get_language
from django.forms.widgets import RadioSelect
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from web.accounts.mixins import PlayerMissionStateContextMixin, MissionContextMixin
from web.core.views import LoginRequiredMixin
from ..models import *
from ..mixins import ChallengeContextMixin

import logging
log = logging.getLogger(__name__)


class FinalBarrierDetailView(LoginRequiredMixin, 
                             PlayerMissionStateContextMixin,
                             MissionContextMixin,
                             ChallengeContextMixin,
                             DetailView):
    model = FinalBarrierChallenge
    template_name = 'challenges/final_barrier_overview.html'
    pk_url_kwarg = 'challenge_id'
    context_object_name = 'challenge'


    def dispatch(self, request, *args, **kwargs):
        self.challenge = get_object_or_404(Challenge, pk=kwargs['challenge_id'])

        # make sure the challenge has not been played yet and is not
        # expired
        if not self.challenge.parent.is_expired and not \
                ChallengeAnswerWithOneChoice.objects.filter(
                                user=request.user, 
                                challenge=self.challenge
                ).exists():
            return redirect(self.challenge.play_url)
        return super(BarrierDetailView, self).dispatch(request,
                                                        *args, **kwargs)


    def get_context_data(self, **kwargs):
        ctx = super(FinalBarrierDetailView, self).get_context_data(**kwargs)
        ctx.update({
            'is_completed': True,
            'mission': self.object.parent,
            'challenges': self.object.parent.get_children(),
        })
        return ctx

final_barrier_detail_view = FinalBarrierDetailView.as_view()


class FinalBarrierForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        challenge = kwargs.get('initial')['challenge']
        super(FinalBarrierForm, self).__init__(*args, **kwargs)

        self.fields['selected'] = forms.ModelChoiceField(
            widget=RadioSelect,
            required=True,
            empty_label=None,
            queryset=ChallengeAnswerChoice.objects.filter(challenge=challenge).distinct()
        )

    class Meta:
        model = ChallengeAnswerWithMultipleChoices
        exclude = ('user', 'challenge')


class FinalBarrierCreateView(LoginRequiredMixin, 
                             PlayerMissionStateContextMixin,
                             MissionContextMixin,
                             ChallengeContextMixin,
                             CreateView):
    form_class = FinalBarrierForm
    model = None
    context_object_name = 'final_barrier_answer'
    template_name = "challenges/final_barrier.html"

    def dispatch(self, request, *args, **kwargs):
        self.challenge = get_object_or_404(Challenge, pk=kwargs['challenge_id'])

        self.initial.update({'challenge': self.challenge,})
        return super(FinalBarrierCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.challenge = self.challenge
        self.object.save()
        return redirect(self.challenge.overview_url)
        #return log_activity_and_redirect(self.request, self.challenge, action_msg)

    def form_invalid(self, form):
        print form.errors
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, *args, **kwargs):
        context_data = super(FinalBarrierCreateView, self).get_context_data(*args, **kwargs)
        context_data.update({
            'challenge': self.challenge,
            'mission': self.challenge.parent,
            'challenges': self.challenge.parent.get_children(),
        })
        return context_data

final_barrier_play_view = FinalBarrierCreateView.as_view()
