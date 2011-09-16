import datetime

from django import forms
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User

from gmapsfield.fields import GoogleMapsField

from web.instances.models import Instance

def list_submodels(parent):
    _models = []
    for model in models.get_models():
        if issubclass(model, parent) and not str(model._meta) == str(parent._meta):
            _models.append( (model.__module__, model._meta.verbose_name) )
    return _models

# Ability for players to create challenges
class AddChallenge(forms.Form):
    map = GoogleMapsField().formfield(label=_('Location'))
    name = forms.CharField(label=_("Name"), max_length=255)
    description = forms.CharField(label=_("Description"), help_text=_('Describe what people have to do to complete the challenge'), widget=forms.Textarea(attrs={'rows': 6, 'cols': 60}))
    start_date = forms.SplitDateTimeField(required=False,
                                          input_time_formats=('%I:%M %p', '%H:%M'),
                                          label=_("Challenge Start Date/Time (optional)"),
                                         )
    end_date = forms.SplitDateTimeField(required=False,
                                        input_time_formats=('%I:%M %p', '%H:%M'),
                                        label=_("Challenge End Date/Time (optional)"),
                                       )

    def __init__(self, instance, *args, **kwargs):
        super(AddChallenge, self).__init__(*args, **kwargs)

    def clean_end_date(self):
        end_date = self.cleaned_data.get('end_date')
        start_date = self.cleaned_data.get('start_date')
        if end_date and start_date:
            # Ensure end date is in the present or the future
            if self.cleaned_data.get('end_date') < datetime.datetime.now():
                raise forms.ValidationError(_("Please enter an end date not in the past."))
            if self.cleaned_data.get('end_date') < self.cleaned_data.get('start_date'):
                raise forms.ValidationError(_("Please enter an end date after the start date."))
        return self.cleaned_data.get('end_date')
