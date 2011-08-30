from django import forms
from web.missions.models import Mission

class MissionAdminForm(forms.ModelForm):
    class Meta:
        model = Mission

    def clean_start_date(self):
        return self.cleaned_data["name"]
