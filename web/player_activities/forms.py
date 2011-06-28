from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.contrib.auth import authenticate
from web.instances.models import Instance
from web.player_activities.models import PlayerActivity
from web.answers.models import *

class OpenForm(forms.Form):
    answerbox = forms.CharField(required=True, widget=forms.Textarea(attrs={"rows": 2, "cols": 40}))
    
    class Meta:
        model = AnswerOpenEnded

class SingleForm(forms.Form):
    class Meta:
        model = AnswerSingleResponse

class MapForm(forms.Form):
    class Meta:
        model = AnswerMap
        
class EmpathyForm(forms.Form):
    class Meta:
        model = AnswerEmpathy
        
