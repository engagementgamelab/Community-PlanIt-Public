from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.utils import simplejson
from django.contrib.auth import authenticate
from web.instances.models import Instance
from web.values.models import Value
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

class ValueBaseForm(forms.Form):
    ins = []
    ins.append((0, '------'))
    for x in Instance.objects.all().order_by("name"):
        ins.append((x.id, x.name))
    instances = forms.ChoiceField(required=False, choices=ins)

class MissionBaseForm(forms.Form):
    ins = []
    ins.append((0, '------'))
    for x in Instance.objects.all().order_by("name"):
        ins.append((x.id, x.name))
    instances = forms.ChoiceField(required=False, choices=ins)

class MissionSaveForm(forms.Form):
    days = forms.IntegerField()
    
class ActivityBaseForm(forms.Form):
    ins = []
    ins.append((0, '------'))
    for x in Instance.objects.all().order_by("name"):
        ins.append((x.id, x.name))
    instances = forms.ChoiceField(required=False, choices=ins)

class ActivitySaveForm(forms.Form):
    missions = forms.ChoiceField()
    
    def __init__(self, *args, **kwargs):
        initial =  kwargs.get("initial", {})
        missions = initial.get("missions", None)
        if missions:
            kwargs['initial']['missions'] = missions[0]
        super(ActivitySaveForm, self).__init__(*args, **kwargs)
        for mission in missions:
            self.fields["missions"].choices.append(mission)

class ActivityEditForm(forms.Form):
    name = forms.CharField()
    question = forms.CharField()
    missions = forms.ChoiceField()
    types = forms.ChoiceField()
    instructions = forms.ChoiceField(required=False)
    addInstructions = forms.ChoiceField(required=False)
    points = forms.IntegerField(required=False)
    attachment = forms.ImageField(required=False)
    
    def __init__(self, *args, **kwargs):
        initial =  kwargs.get("initial", {})
        missions = initial.get("missions", None)
        types = initial.get("types", None)
        
        if missions:
            kwargs['initial']['missions'] = missions[0]
        if types:
            kwargs['initial']['types'] = types[0]
        
        super(ActivityEditForm, self).__init__(*args, **kwargs)
        for mission in missions:
            self.fields["missions"].choices.append(mission)
        
        for type in types:
            self.fields["types"].choices.append(mission)

    