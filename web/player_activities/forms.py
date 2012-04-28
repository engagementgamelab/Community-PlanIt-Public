from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple
from django.utils import simplejson
from django.utils.translation import ugettext as _
from gmapsfield.fields import *

from .models import PlayerActivity, PlayerActivityType, MultiChoiceActivity
from instances.models import Instance
from missions.models import Mission
from answers.models import *


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
    answ3 = forms.CharField(required=True, max_length=255, label=_("Answer c)"))
    answ4 = forms.CharField(required=True, max_length=255, label=_("Answer d)"))
    answ5 = forms.CharField(required=True, max_length=255, label=_("Answer e)"))

    class Meta:
        exclude = ('activity',)


