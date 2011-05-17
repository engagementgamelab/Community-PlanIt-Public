from django import forms

from web.responses.choices.models import *

class ChoicesResponseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ChoicesResponseForm, self).__init__(*args, **kwargs)
        qs = kwargs.get('instance').choices.all()
        self.fields['choices'] = forms.ModelChoiceField(queryset=qs, help_text='',
                widget=forms.RadioSelect, initial=qs[0].id, error_messages={'required': 'Please select a valid response.'})

    class Meta:
        model = ChoicesResponse
        fields = ('choices',)
    
    def clean(self):
        choices = self.cleaned_data.get('choices')
        self.cleaned_data['choices'] = choices

        return self.cleaned_data
