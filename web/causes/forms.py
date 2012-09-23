from django import forms 
from django.utils.translation import get_language, ugettext, ugettext_lazy as _

from .models import Cause

class CauseForm(forms.ModelForm):
	facebook_group_url = forms.URLField(widget=forms.TextInput(attrs={
        'placeholder': 'Facebook Group URL',
    }), label=_("Facebook Group"), max_length=300)

	class Meta:
		model = Cause
		exclude = ('creator', 'instance')
