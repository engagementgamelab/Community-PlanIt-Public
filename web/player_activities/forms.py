from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.contrib.auth import authenticate
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple
from django.utils import simplejson
from web.instances.models import Instance
from web.player_activities.models import PlayerActivity
from web.answers.models import *

from gmapsfield.fields import *

def make_openended_form():

    class OpenEndedForm(forms.Form):
        message = forms.CharField(widget=forms.Textarea)
        class Meta:
            model = AnswerOpenEnded
    return OpenEndedForm

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

