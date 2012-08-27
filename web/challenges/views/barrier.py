from django import forms
from django.utils.translation import get_language
from django.forms.widgets import RadioSelect
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from ..models import *
from web.core.views import LoginRequiredMixin

import logging
log = logging.getLogger(__name__)


class FetchAnswersMixin(object):

    def get_context_data(self, *args, **kwargs):
        ctx = super(FetchAnswersMixin, self).\
                get_context_data(*args, **kwargs)
        print '1) %s get_ctx' % self.__class__.__name__
        return ctx


class BarrierDetailView(LoginRequiredMixin, FetchAnswersMixin, DetailView):
    model = BarrierChallenge
    template_name = 'challenges/barrier_overview.html'
    pk_url_kwarg = 'challenge_id'
    context_object_name = 'challenge'

    def get_context_data(self, **kwargs):
        ctx = super(BarrierDetailView, self).get_context_data(**kwargs)
        ctx.update({
            'is_completed': True,
            'mission': self.object.parent,
            'challenges': self.object.parent.get_children(),
        })
        return ctx

barrier_detail_view = BarrierDetailView.as_view()


class BarrierForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        challenge = kwargs.get('initial')['challenge']
        super(BarrierForm, self).__init__(*args, **kwargs)

        self.fields['selected'] = forms.ModelChoiceField(
            widget=RadioSelect,
            required=True,
            empty_label=None,
            queryset=AnswerChoice.objects.filter(challenge=challenge).distinct()
        )

    class Meta:
        model = AnswerWithChoices
        exclude = ('user', 'challenge')


class RedirectToChallengeOverviewMixin(object):

    def dispatch(self, request, *args, **kwargs):
        if AnswerWithChoices.objects.filter(user=request.user, challenge=self.challenge).exists():
            return redirect(self.challenge.overview_url)

        return super(RedirectToChallengeOverviewMixin, self).dispatch(request, *args, **kwargs)


class BarrierCreateView(LoginRequiredMixin, RedirectToChallengeOverviewMixin, CreateView):
    form_class = BarrierForm
    model = None
    context_object_name = 'barrier_answer'
    template_name = "challenges/barrier.html"

    def dispatch(self, request, *args, **kwargs):
        self.challenge = get_object_or_404(Challenge, pk=kwargs['challenge_id'])

        self.initial.update({'challenge': self.challenge,})
        return super(BarrierCreateView, self).dispatch(request, *args, **kwargs)

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
        context_data = super(BarrierCreateView, self).get_context_data(*args, **kwargs)
        context_data.update({
            'challenge': self.challenge,
            'challenges': self.challenge.parent.get_children(),
            'mission': self.challenge.parent,
        })
        return context_data

barrier_play_view = BarrierCreateView.as_view()
