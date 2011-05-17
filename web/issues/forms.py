from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.contrib.auth import authenticate
from web.instances.models import Instance
from web.issues.models import Issue

class UserProfileForm(forms.ModelForm):
    
    class Meta:
        model = Issue
        include = ( 'message' )
