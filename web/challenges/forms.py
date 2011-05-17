import datetime
from django import forms
from django.db import models
from django.contrib.auth.models import User

from web.instances.models import Instance
from web.responses.models import Response

from gmapsfield.fields import GoogleMapsField

def list_submodels(parent):
    _models = []
    for model in models.get_models():
        if issubclass(model, parent) and not str(model._meta) == str(parent._meta):
            _models.append( (model.__module__, model._meta.verbose_name) )
    return _models

# Ability for players to create challenges
class AddChallenge(forms.Form):
    map = GoogleMapsField().formfield(label='Plot your challenge on the map', help_text="<p>Where will your challenge take place?</p>")
    name = forms.CharField(label="Challenge Name", help_text='<br>What is the name of your challenge?', max_length=255)
    description = forms.CharField(label="Challenge Description", help_text='<br>Describe what people have to do to complete the challenge', widget=forms.Textarea)
    start_date = forms.DateTimeField(label="Challenge Start", help_text='<br>When will your challenge start?')
    end_date = forms.DateTimeField(label="Challenge End", help_text='<br>When will your challenge end? (cannot be the same as start)')

    def clean(self):
        # Ensure end date is in the present or the future
        if self.cleaned_data.get('end_date') < datetime.datetime.now():
            raise forms.ValidationError("Please enter an end date not in the past.")

        return self.cleaned_data
