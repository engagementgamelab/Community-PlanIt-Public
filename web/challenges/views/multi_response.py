from django import forms
from django.utils.translation import get_language
from django.forms.widgets import CheckboxSelectMultiple
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from web.core.views import LoginRequiredMixin
from web.missions.models import Mission
from ..models import *
from ..mixins import PlayerMissionStateContextMixin

import logging
log = logging.getLogger(__name__)


class FetchAnswersMixin(object):

    def get_context_data(self, *args, **kwargs):
        ctx = super(FetchAnswersMixin, self).\
                get_context_data(*args, **kwargs)
        print '1) %s get_ctx' % self.__class__.__name__
        return ctx


class MultiResponseDetailView(LoginRequiredMixin, 
                              DetailView, PlayerMissionStateContextMixin):
    model = MultiResponseChallenge
    template_name = 'challenges/multi_overview.html'
    #queryset = Instance.objects.exclude(is_disabled=True)
    pk_url_kwarg = 'challenge_id'
    context_object_name = 'challenge'

    def dispatch(self, request, *args, **kwargs):
        self.challenge = get_object_or_404(Challenge, pk=kwargs['challenge_id'])
        self.mission = get_object_or_404(Mission, pk=kwargs['mission_id'])

        # make sure the challenge has not been played yet and is not
        # expired
        if not self.challenge.parent.is_expired and not \
                AnswerWithMultipleChoices.objects.filter(
                                user=request.user, 
                                challenge=self.challenge
                ).exists():
            return redirect(self.challenge.play_url)
        return super(MultiResponseDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(MultiResponseDetailView, self).\
                get_context_data(**kwargs)
        my_answers = AnswerWithMultipleChoices.objects.get(
                                user=self.request.user,
                                challenge=self.object
        )
        ctx.update({
            'my_answers': my_answers,
        })
        print ctx
        return ctx

multi_response_detail_view = MultiResponseDetailView.as_view()


class MultiResponseForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        challenge = kwargs.get('initial')['challenge']
        super(MultiResponseForm, self).__init__(*args, **kwargs)

        self.fields['selected'] = forms.ModelMultipleChoiceField(
                    widget=CheckboxSelectMultiple,
                    required=True,
                    queryset=AnswerChoice.objects.\
                            filter(challenge=challenge).distinct()
        )

    class Meta:
        model = AnswerWithMultipleChoices
        exclude = ('user', 'challenge')


class MultiResponseCreateView(LoginRequiredMixin, 
                               CreateView, PlayerMissionStateContextMixin):
    form_class = MultiResponseForm
    model = None
    context_object_name = 'multi_response_answer'
    template_name = "challenges/multi.html"

    def dispatch(self, request, *args, **kwargs):
        self.challenge = get_object_or_404(MultiResponseChallenge, pk=kwargs['challenge_id'])

        if AnswerWithMultipleChoices.objects.\
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
                get_context_data(*args, **kwargs)
        context_data.update({
            'challenge': self.challenge,
            'mission': self.challenge.parent,
        })
        return context_data

multi_response_play_view = MultiResponseCreateView.as_view()
