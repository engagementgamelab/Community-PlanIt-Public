from django import forms
from django.utils.translation import get_language
from django.forms.widgets import CheckboxSelectMultiple
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


class MultiResponseDetailView(LoginRequiredMixin, FetchAnswersMixin, DetailView):
    model = MultiResponseChallenge
    template_name = 'challenges/multi_overview.html'
    #queryset = Instance.objects.exclude(is_disabled=True)
    pk_url_kwarg = 'challenge_id'
    context_object_name = 'challenge'

    def get_context_data(self, **kwargs):
        ctx = super(MultiResponseDetailView, self).\
                get_context_data(**kwargs)
        ctx.update({
            #'activity' : kwargs['activity'],
            'is_completed': True,
            'mission': self.object.parent,
            'challenges': self.object.parent.challenges.all(),
        })
        print ctx
        print '2) %s get_ctx' % self.__class__.__name__
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
        model = AnswerWithChoices
        exclude = ('user',)


class RedirectToChallengeOverviewMixin(object):

    def dispatch(self, request, *args, **kwargs):
        if AnswerWithChoices.objects.\
                filter(user=request.user, challenge=self.challenge).\
                exists():
            return redirect(self.challenge.overview_url)

        return super(RedirectToChallengeOverviewMixin, self).dispatch(request,
            *args, **kwargs)


class MultiResponseCreateView(LoginRequiredMixin, 
                               RedirectToChallengeOverviewMixin, 
                               CreateView):
    form_class = MultiResponseForm
    model = None
    context_object_name = 'multi_response_answer'
    template_name = "challenges/multi.html"

    def dispatch(self, request, *args, **kwargs):
        self.challenge = get_object_or_404(MultiResponseChallenge, pk=kwargs['challenge_id'])
        self.initial.update({'challenge': self.challenge,})
        return super(MultiResponseCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        #self.object.challenge = self.challenge
        self.object.save()
        return redirect(self.challenge.overview_url)
        #return log_activity_and_redirect(self.request, self.challenge, action_msg)

    def form_invalid(self, form):
        print form.errors
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, *args, **kwargs):
        context_data = super(MultiResponseCreateView, self).\
                get_context_data(*args, **kwargs)
        context_data.update({
            'challenge': self.challenge,
            'mission': self.challenge.parent,
            'challenges': self.challenge.parent.challenges.all(),
        })
        print '%s get_ctx' % self.__class__.__name__
        return context_data

multi_response_play_view = MultiResponseCreateView.as_view()
