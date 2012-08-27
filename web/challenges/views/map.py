import simplejson 
from django import forms
from django.utils.translation import get_language
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


class MapDetailView(LoginRequiredMixin, FetchAnswersMixin, DetailView):
    model = MapChallenge
    template_name = 'challenges/map_overview.html'
    #queryset = Instance.objects.exclude(is_disabled=True)
    pk_url_kwarg = 'challenge_id'
    context_object_name = 'challenge'

    def get_context_data(self, **kwargs):
        ctx = super(MapDetailView, self).\
                get_context_data(**kwargs)
        ctx.update({
            #'activity' : kwargs['activity'],
            'is_completed': True,
            'mission': self.object.parent,
            'challenges': self.object.parent.get_children(),
        })
        print ctx
        print '2) %s get_ctx' % self.__class__.__name__
        return ctx

map_detail_view = MapDetailView.as_view()


class MapForm(forms.ModelForm):
    map = GoogleMapsField().formfield()

    def clean_map(self):
        map = self.cleaned_data.get('map')
        if not map:
            raise forms.ValidationError("The map doesn't exist")
        mapDict = simplejson.loads(map);
        if len(mapDict["markers"]) == 0:
            raise forms.ValidationError("Please select a point on the map")
        return map

    class Meta:
        model = AnswerMap
        exclude = ('user', 'challenge')

class MultiResponseForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        challenge = kwargs.get('initial')['challenge']
        super(MultiResponseForm, self).__init__(*args, **kwargs)

        self.fields['selected'] = forms.ModelChoiceField(
                    widget=CheckboxSelectMultiple,
                    required=True,
                    empty_label=None,
                    queryset=MultiChoiceActivity.objects.\
                            language(get_language()).\
                            filter(activity=challenge).distinct()
        )

    class Meta:
        model = AnswerMap
        exclude = ('user',)


class RedirectToChallengeOverviewMixin(object):

    def dispatch(self, request, *args, **kwargs):
        if AnswerMap.objects.\
                filter(user=request.user).\
                exists():
            return redirect(self.challenge.overview_url)

        return super(RedirectToChallengeOverviewMixin, self).dispatch(request,
            *args, **kwargs)


class MapCreateView(LoginRequiredMixin, 
                               RedirectToChallengeOverviewMixin, 
                               CreateView):
    form_class = MapForm
    model = None
    context_object_name = 'map_answer'
    template_name = "challenges/map.html"

    def dispatch(self, request, *args, **kwargs):
        self.challenge = get_object_or_404(MapChallenge, pk=kwargs['challenge_id'])
        self.initial.update({'challenge': self.challenge,})
        return super(MapCreateView, self).dispatch(request, *args, **kwargs)

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
        context_data = super(MapCreateView, self).\
                get_context_data(*args, **kwargs)
        context_data.update({
            'challenge': self.challenge,
            'mission': self.challenge.parent,
            'challenges': self.challenge.parent.get_children(),
        })
        return context_data

map_play_view = MapCreateView.as_view()
