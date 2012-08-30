from django import forms
from django.utils.translation import get_language
from django.forms.widgets import RadioSelect
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from web.missions.models import Mission
from web.core.views import LoginRequiredMixin
from ..models import *
from ..mixins import PlayerMissionStateContextMixin

import logging
log = logging.getLogger(__name__)

#class RedirectToChallengeOverviewMixin(object):
#    def dispatch(self, request, *args, **kwargs):
#        if AnswerWithChoices.objects.\
#                filter(user=request.user, challenge=self.challenge).\
#                exists():
#            return redirect(self.challenge.overview_url)
#        return super(RedirectToChallengeOverviewMixin, self).dispatch(request,
#            *args, **kwargs)
#class FetchAnswersMixin(object):
#    def get_context_data(self, *args, **kwargs):
#        ctx = super(FetchAnswersMixin, self).\
#                get_context_data(*args, **kwargs)
#        return ctx


class SingleResponseDetailView(LoginRequiredMixin, 
                               DetailView, PlayerMissionStateContextMixin):

    model = SingleResponseChallenge
    template_name = 'challenges/single_overview.html'
    #queryset = Instance.objects.exclude(is_disabled=True)
    pk_url_kwarg = 'challenge_id'
    context_object_name = 'challenge'

    def dispatch(self, request, *args, **kwargs):
        self.challenge = get_object_or_404(Challenge, pk=kwargs['challenge_id'])
        self.mission = get_object_or_404(Mission, pk=kwargs['mission_id'])

        # make sure the challenge has not been played yet and is not
        # expired
        if not self.challenge.parent.is_expired and not \
                AnswerWithOneChoice.objects.filter(
                                user=request.user, 
                                challenge=self.challenge
                ).exists():
            return redirect(self.challenge.play_url)
        return super(SingleResponseDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(SingleResponseDetailView, self).\
                get_context_data(**kwargs)
        my_answer = AnswerWithOneChoice.objects.get(
                                user=self.request.user,
                                challenge=self.object
        )
        ctx.update({
            'my_answer': my_answer,
        })
        return ctx

single_response_detail_view = SingleResponseDetailView.as_view()


class SingleResponseForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        challenge = kwargs.get('initial')['challenge']
        super(SingleResponseForm, self).__init__(*args, **kwargs)

        self.fields['selected'] = forms.ModelChoiceField(
                    widget=RadioSelect,
                    required=True,
                    empty_label=None,
                    queryset=AnswerChoice.objects.\
                            filter(challenge=challenge).distinct()
        )

    class Meta:
        model = AnswerWithOneChoice
        exclude = ('user', 'challenge')


class SingleResponseCreateView(LoginRequiredMixin,
                               CreateView, PlayerMissionStateContextMixin):

    form_class = SingleResponseForm
    model = None
    context_object_name = 'single_response_answer'
    template_name = "challenges/single.html"

    def dispatch(self, request, *args, **kwargs):
        self.challenge = get_object_or_404(Challenge, pk=kwargs['challenge_id'])

        if AnswerWithOneChoice.objects.\
                        filter(user=request.user, challenge=self.challenge).\
                        exists():
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
                get_context_data(*args, **kwargs)
        context_data.update({
            'challenge': self.challenge,
            'mission': self.challenge.parent,
        })
        return context_data

single_response_play_view = SingleResponseCreateView.as_view()
