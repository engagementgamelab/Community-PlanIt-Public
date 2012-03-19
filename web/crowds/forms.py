import datetime
from gmapsfield.fields import GoogleMapsField

from django import forms
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from instances.models import Instance
from crowds.models import Crowd

# Ability for players to create crowds
class CrowdForm(forms.ModelForm):

    map = GoogleMapsField().formfield(label=_('Location'))
    start_date = forms.SplitDateTimeField(required=False,
                                          input_time_formats=('%I:%M %p', '%H:%M'),
                                          label=_("When? (time of event)"),
                                         )
    end_date = forms.SplitDateTimeField(required=False,
                                          input_time_formats=('%I:%M %p', '%H:%M'),
                                          label=_("Till When? (end time of event)"),
                                         )

    def __init__(self, *args, **kwargs):
        #import ipdb;ipdb.set_trace()
        #self.fields['description'].help_text=_('What do you want to accomplish?')
        super(CrowdForm, self).__init__(*args, **kwargs)


    class Meta:
        model = Crowd
        exclude = ('instance', 'participants', 'creator', 'flagged', 'attachments', 'comments',)


