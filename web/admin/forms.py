from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.utils import simplejson
from django.contrib.auth import authenticate
from web.instances.models import Instance
from gmapsfield.fields import GoogleMapsField

class InstanceBaseForm(forms.Form):
    ins = []
    ins.append((0, '------'))
    for x in Instance.objects.all().order_by("name"):
        ins.append((x.id, x.name))
    instances = forms.ChoiceField(required=False, choices=ins)
    instance_name = forms.CharField(required=False, max_length=45)
    
    #def clean(self):
    #    instances
    
class InstanceEditForm(forms.Form):
    name = forms.CharField(required=True, max_length=45)
    start_date = forms.DateTimeField(required=True)
    end_date = forms.DateTimeField(required=True)
    location = GoogleMapsField().formfield()
    
    def clean_location(self):
        location = self.cleaned_data.get("location")
        if location == None:
            {"frozen": null, "zoom": 13, "markers": null, "coordinates": [42.36475475505694, -71.05134683227556], "size": [500, 400]}
        raise forms.ValidationError("location: %s" % location)
        if not location or not simplejson.loads(location).has_key('coordinates'):
          raise forms.ValidationError('Please make a selection on the map.')

        return self.cleaned_data

    