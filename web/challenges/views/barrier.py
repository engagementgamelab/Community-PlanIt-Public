from django import forms
from django.utils.translation import get_language
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode
from django.utils.html import conditional_escape

from ..models import *
from web.core.views import LoginRequiredMixin

import logging
log = logging.getLogger(__name__)


class FetchAnswersMixin(object):

    def get_context_data(self, *args, **kwargs):
        ctx = super(FetchAnswersMixin, self).\
                get_context_data(*args, **kwargs)
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


class RedirectToChallengeOverviewMixin(object):

    def dispatch(self, request, *args, **kwargs):
        if AnswerWithMultipleChoices.objects.filter(
                                    user=request.user,
                                    challenge=self.challenge
                ).exists():
            return redirect(self.challenge.overview_url)

        return super(RedirectToChallengeOverviewMixin, self).dispatch(request, *args, **kwargs)


class BarrierRadioInput(forms.widgets.RadioInput):

    def __init__(self, *args, **kwargs):
        choice_statuses = kwargs.pop('choice_statuses')
        super(BarrierRadioInput, self).__init__(*args, **kwargs)

    def render(self, name=None, value=None, attrs=None, choices=()):
        name = name or self.name
        value = value or self.value
        attrs = attrs or self.attrs
        if 'id' in self.attrs:
            label_for = ' for="%s_%s"' % (self.attrs['id'], self.index)
        else:
            label_for = ''
        choice_label = conditional_escape(force_unicode(self.choice_label))

        dark_background_css = 'class="radio-item-disabled"'
        #background: none repeat scroll 0 0 #DDDDDD;"'

        return mark_safe(u'<label%s %s>%s %s</label>' % (label_for, dark_background_css, self.tag(), choice_label))

class BarrierFieldRenderer(forms.widgets.RadioFieldRenderer):

    """ Modifies some of the Radio buttons to be disabled in HTML,
    based on an externally-appended choice_statuses list. """

    def __iter__(self):
        for i, choice in enumerate(self.choices):
            yield BarrierRadioInput(self.name, self.value, self.attrs.copy(), choice, i, choice_statuses=self.choice_statuses)

    def render(self):
        if not hasattr(self, "choice_statuses"):
            return self.original_render()
        return self.my_render()

    def original_render(self):
        return mark_safe(u'<ul>\n%s\n</ul>' % u'\n'.join([u'<li>%s</li>'
            % force_unicode(w) for w in self]))

    def my_render(self):
        midList = []
        for x, wid in enumerate(self):
            if self.choice_statuses[x]:
                wid.attrs['disabled'] = True
            midList.append(u'<li>%s</li>' % force_unicode(wid))
        finalList = mark_safe(u'<ul>\n%s\n</ul>' % u'\n'.join([u'<li>%s</li>'
            % w for w in midList])
        )
        return finalList


class BarrierForm(forms.Form):

    def __init__(self, *args, **kwargs):
        instance = kwargs.pop('instance')
        initial_data = kwargs.pop('initial')
        challenge = initial_data.get('challenge')
        super(BarrierForm, self).__init__(*args, **kwargs)
        answers = AnswerChoice.objects.by_challenge(challenge)#.distinct()

        choices = answers.values_list('pk', 'value')
        self.fields['selected'] = forms.ChoiceField(required=True)
        self.fields['selected'].widget = forms.widgets.RadioSelect(
                renderer=BarrierFieldRenderer, choices=choices
        )
        self.fields['selected'].widget.renderer.choice_statuses = challenge.random_answer_choices

    class Meta:
        #model = AnswerWithMultipleChoices
        exclude = ('user', 'challenge')


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
