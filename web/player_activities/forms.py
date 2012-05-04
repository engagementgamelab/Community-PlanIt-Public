from localeurl.models import reverse
from stream import utils as stream_utils
from gmapsfield.fields import *

from django import forms
from django.core.cache import cache
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.formtools.wizard.views import SessionWizardView
from django.shortcuts import redirect
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple
from django.utils import simplejson
from django.utils.translation import ugettext as _

from .models import PlayerActivity, PlayerMapActivity, PlayerActivityType, MultiChoiceActivity
from web.instances.models import Instance
from web.missions.models import Mission
from web.answers.models import *
from web.core.utils import missions_bar_context

import logging
log = logging.getLogger(__name__)

def make_answer_form():
    class AnswerForm(forms.Form):
        response = forms.CharField(widget=forms.Textarea)
        class Meta:
            model = Answer
    return AnswerForm

def make_openended_form():
    class OpenEndedAnswerForm(forms.Form):
        response = forms.CharField(widget=forms.Textarea)
        class Meta:
            model = AnswerOpenEnded
    return OpenEndedAnswerForm

def make_empathy_form():
    class EmpathyAnswerForm(forms.Form):
        response = forms.CharField(widget=forms.Textarea)
        class Meta:
            model = AnswerEmpathy
    return EmpathyAnswerForm

def make_single_form(choices):
    class SingleForm(forms.Form):
        response = forms.ChoiceField(widget=RadioSelect, choices=choices)
        class Meta:
            model = AnswerSingleResponse
    return SingleForm

def make_multi_form(choices):
    class MultiForm(forms.Form):
        response = forms.ChoiceField(widget=CheckboxSelectMultiple, choices=choices, required=False)
        class Meta:
            model = AnswerMultiChoice
    return MultiForm

class MapForm(forms.Form):
    map = GoogleMapsField().formfield()

    def clean_map(self):
        map = self.cleaned_data.get('map')
        if not map:
            raise forms.ValidationError("The map doesn't exist")
        mapDict = simplejson.loads(map);
        if len(mapDict["markers"]) == 0:
            raise forms.ValidationError("Please select a point on the map")
        return map

# =========================================
# player submitted activity wizard and forms

class SelectNewActivityForm(forms.Form):

    #mission = forms.ModelChoiceField(
    #            queryset=Mission.objects.filter()
    #)
    name = forms.CharField(required=True, max_length=255, label=_("Name"))
    question = forms.CharField(required=True, max_length=1000, label=_("Question"))
    #type = forms.ChoiceField(
    #            choices=PlayerActivityType.objects.filter(
    #                    type__in=['open_ended', 'multi_response', 'map']
    #                    ).values_list('type', 'displayType')
    #)
    type = forms.ModelChoiceField(required=True,
                                label = _("Select Type of Challenge"),
                                queryset = PlayerActivityType.objects.filter(
                                        type__in=['open_ended', 'multi_response', 'map']
                                        )  #.values_list('type', 'displayType')
    )

class MultiResponseForm(forms.Form):

    answ1 = forms.CharField(required=True, max_length=255, label=_("Answer a)"))
    answ2 = forms.CharField(required=True, max_length=255, label=_("Answer b)"))
    answ3 = forms.CharField(required=False, max_length=255, label=_("Answer c)"))
    answ4 = forms.CharField(required=False, max_length=255, label=_("Answer d)"))
    answ5 = forms.CharField(required=False, max_length=255, label=_("Answer e)"))

    #class Meta:
    #    exclude = ('activity',)


class NewActivityWizard(SessionWizardView):


    def process_step(self, form):
        form_list = self.get_form_list()
        cd =  form.cleaned_data
        if len(form_list.keys()) == 1:
            d = {
                    'multi_response': MultiResponseForm,
                    #'map' : MapForm,
            }
            next_form = d.get(cd.get('type').type)
            if next_form:
                self.form_list.update({'1': next_form})
        return self.get_form_step_data(form)

    def get_context_data(self, form, **kwargs):
        context = super(NewActivityWizard, self).get_context_data(form, **kwargs)
        context.update({ 'game_header' : True, })
        context.update(missions_bar_context(self.request))

        form_list = self.get_form_list()
        if len(form_list.keys()) > 1:
            if form_list.get('1') == MultiResponseForm:
                self.template_name = 'player_activities/new_multi_response.html'
            #elif form_list.get('1') == MapForm:
            #    self.template_name =  'player_activities/new_map.html'

            #    mission = Mission.objects.get(slug="growth-versus-proficiency")
            #    init_coords = []
            #    map = mission.instance.location
            #    markers = simplejson.loads("%s" % map)["markers"]
            #    x = 0
            #    for coor in markers if markers != None else []:
            #        coor = coor["coordinates"]
            #        init_coords.append( [x, coor[0], coor[1]] )
            #        x = x + 1
            #    context.update(dict(
            #            init_coords = init_coords,
            #            map = map,
            #    ))
        else:
            self.template_name =  'player_activities/new_activity_form1.html'

        return context

    def done(self, form_list, **kwargs):

        mission_slug = kwargs.pop('mission_slug', '')

        form_one = form_list[0]

        type = PlayerActivityType.objects.get(type=form_one.cleaned_data.get('type'))
        mission = Mission.objects.get(slug=mission_slug)
        q = form_one.cleaned_data.get('question', '')

        if type.type == 'map':
            activity_cls = PlayerMapActivity
        elif type.type in ['multi_response', 'open_ended']:
            activity_cls = PlayerActivity

        create_kwargs =dict( 
                mission=mission,
                creationUser=self.request.user,
                type=type,
                question=q,
                points=0,
                is_player_submittd=True,
                name = form_one.cleaned_data.get('name', ''),
        )
        new_activity = activity_cls.objects.create(**create_kwargs)

        if type.type == 'multi_response':
            form_two = form_list[1]
            log.debug("player submitted multi:%s " % form_two.cleaned_data)
            for f in form_two.cleaned_data.keys():
                if form_two.cleaned_data.get(f).strip() != '':
                    mc = MultiChoiceActivity.objects.create(
                            value=form_two.cleaned_data.get(f, ''),
                            activity=new_activity,
                    )
        cache.invalidate_group('activities_for_mission')
        stream_utils.action.send(
                                self.request.user,
                                verb='activity_player_submitted',
                                action_object=new_activity,
                                target=self.request.current_game,
                                description='player submitted a challenge',
        )
        return redirect(reverse("missions:mission", args=(mission.slug,)))
