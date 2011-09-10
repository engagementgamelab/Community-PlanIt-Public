import datetime
from django import forms
from django.db import models
from django.contrib.auth.models import User

from web.instances.models import Instance

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
    start_date = forms.SplitDateTimeField(required=False,
                                          input_time_formats=('%I:%M %p', '%H:%M'),
                                          label="Challenge Start",
                                          help_text='When will your challenge start?'
                                         )
    end_date = forms.SplitDateTimeField(required=False,
                                        input_time_formats=('%I:%M %p', '%H:%M'),
                                        label="Challenge End",
                                        help_text='When will your challenge end? (cannot be the same as start)'
                                       )

    def __init__(self, instance, *args, **kwargs):
        super(AddChallenge, self).__init__(*args, **kwargs)

    def clean_end_date(self):
        end_date = self.cleaned_data.get('end_date')
        start_date = self.cleaned_data.get('start_date')
        if end_date and start_date:
            # Ensure end date is in the present or the future
            if self.cleaned_data.get('end_date') < datetime.datetime.now():
                raise forms.ValidationError("Please enter an end date not in the past.")
            if self.cleaned_data.get('end_date') < self.cleaned_data.get('start_date'):
                raise forms.ValidationError("Please enter an end date after the start date.")
        return self.cleaned_data.get('end_date')
