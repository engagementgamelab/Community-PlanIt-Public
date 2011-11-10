from django import forms
from django.db import models

from instances.models import NotificationRequest

class NotificationRequestForm(forms.ModelForm):

    class Meta:
        model = NotificationRequest
        fields = ['email']

    def __init__(self, community, *args, **kwargs):
        self.community = community
        super(NotificationRequestForm, self).__init__(*args, **kwargs)

    def clean(self):
        if self.community.is_active():
            raise forms.ValidationError('This community is already active. You can sign up right now!')

        if self.community.is_expired():
            raise forms.ValidationError('Sorry, this community is no longer active.')

        return self.cleaned_data
