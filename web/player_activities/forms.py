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
        response = forms.ChoiceField(widget=CheckboxSelectMultiple, choices=choices)
        class Meta:
            model = AnswerMultiChoice
    return MultiForm

class MapForm(forms.Form):
    map = GoogleMapsField()

    def clean(self):
        map = self.cleaned_data.get('map')
        if not map or not simplejson.loads(map).has_key('coordinates'):
          raise forms.ValidationError('Please make a selection on the map.')
        return self.cleaned_data

    class Meta:
        model = AnswerMap
        fields = ('map',)
                
class EmpathyForm(forms.Form):
    class Meta:
        model = AnswerEmpathy
        
