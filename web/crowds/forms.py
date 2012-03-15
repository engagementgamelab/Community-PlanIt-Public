import datetime

from django import forms
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User

from gmapsfield.fields import GoogleMapsField

from instances.models import Instance

def list_submodels(parent):
    _models = []
    for model in models.get_models():
        if issubclass(model, parent) and not str(model._meta) == str(parent._meta):
            _models.append( (model.__module__, model._meta.verbose_name) )
    return _models

# Ability for players to create crowds
class CrowdForm(forms.Form):
    map = GoogleMapsField().formfield(label=_('Location'))
    name = forms.CharField(label=_("Name"), max_length=255)
    description = forms.CharField(label=_("Description"), help_text=_('What do you want to accomplish?'), widget=forms.Textarea(attrs={'rows': 6, 'cols': 60}))
    start_date = forms.SplitDateTimeField(required=False,
                                          input_time_formats=('%I:%M %p', '%H:%M'),
                                          label=_("When? (time of event)"),
                                         )
    confirmation_code = forms.CharField(label=_("Confirmation Code"), max_length=255)

    def __init__(self, instance, *args, **kwargs):
        super(AddChallenge, self).__init__(*args, **kwargs)


