from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.contrib.auth import authenticate
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple
from web.instances.models import Instance
from web.player_activities.models import PlayerActivity
from web.answers.models import *

from gmapsfield.fields import *

class OpenForm(forms.Form):
    answerbox = forms.CharField(required=True, widget=forms.Textarea(attrs={"rows": 2, "cols": 40}))
    
    class Meta:
        model = AnswerOpenEnded

def MakeSingleForm(choices):
    class SingleForm(forms.Form):
        response = forms.ChoiceField(widget=RadioSelect, choices=choices)
        class Meta:
            model = AnswerSingleResponse
    return SingleForm

def MakeMultiForm(choices):
    class MultiForm(forms.Form):
        response = forms.ChoiceField(widget=CheckboxSelectMultiple, choices=choices, required=False)
        class Meta:
            model = AnswerMultiChoice
    return MultiForm

class MapForm(forms.ModelForm):
    map = GoogleMapsField()
    answerBox = forms.CharField(required=True, widget=forms.Textarea(attrs={"rows": 2, "cols": 40}))

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
        fields = ('map', 'answerBox')
                
class EmpathyForm(forms.Form):
    answerBox = forms.CharField(required=True, widget=forms.Textarea(attrs={"rows": 4, "cols": 60}))
    class Meta:
        model = AnswerEmpathy
        
