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
    #This has to be named map, there can be only one and I am guessing it's a huge JS hack to make this work
    map = GoogleMapsField().formfield()
    
    
    def clean_map(self):
        map = self.cleaned_data.get('map')
        if not map:
            raise forms.ValidationError("The map doesn't exist")
        mapDict = simplejson.loads(map)
        if len(mapDict["markers"]) == 0:
            raise forms.ValidationError("Please select a point on the map")
        return map


    