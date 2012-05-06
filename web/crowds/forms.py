import datetime
from gmapsfield.fields import GoogleMapsField

from django.utils import simplejson
from django import forms
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from instances.models import Instance
from crowds.models import Crowd

# Ability for players to create crowds
class CrowdForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Awesome Community Event!'}))
    description = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': 'Let\'s finally get something done! Here\'s what we\'ll do...'}
    ))
    map = GoogleMapsField().formfield(label=_('Location'))
    start_date = forms.SplitDateTimeField(required=False,
                                          input_time_formats=('%I:%M %p', '%H:%M'),
                                          label=_("When? (Start Date/Time of Event)"),
                                         )
    end_date = forms.SplitDateTimeField(required=False,
                                          input_time_formats=('%I:%M %p', '%H:%M'),
                                          label=_("Till When? (End Date/Time of Event)"),
                                         )

    class Meta:
        model = Crowd
        exclude = ('instance', 
                #'confirmation_code', 
                'participants', 'creator', 'flagged', 'attachments', 'comments',
                'address',
        )

    def clean_map(self):
        map = self.cleaned_data.get('map')
        if not map:
            raise forms.ValidationError("The map doesn't exist")
        mapDict = simplejson.loads(map);
        if len(mapDict["markers"]) == 0:
            raise forms.ValidationError("Please select a point on the map")
        return map

    def clean(self):
        cd = self.cleaned_data
        if cd.get('start_date') > cd.get('end_date'):
            self._errors['start_date'] = self.error_class([_("Start Time of Event must come before End Time of Event.")])
            del cd['start_date']
        return cd


