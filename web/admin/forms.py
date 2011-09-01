from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.utils import simplejson
from django.contrib.auth import authenticate
from web.instances.models import Instance
from web.values.models import Value
from accounts.models import CPIUser

from gmapsfield.fields import GoogleMapsField

from nani.forms import TranslatableModelForm
from nani.utils import get_cached_translation, get_translation

import logging
log = logging.getLogger(__name__)

class StaffBaseForm(forms.Form):
    admin_first_name = forms.CharField(required=True, max_length=45)
    admin_last_name = forms.CharField(required=True, max_length=45)
    admin_email = forms.CharField(required=True, max_length=45)
    admin_temp_pass = forms.CharField(widget=forms.PasswordInput(), required=True)
    admin_temp_pass_again = forms.CharField(widget=forms.PasswordInput(), required=True)
    instances = forms.ChoiceField(required=False)
    
    def __init__(self, *args, **kwargs):
        initial =  kwargs.get("initial", {})
        instances = initial.get("instances", None)
        if instances:
            kwargs['initial']['instances'] = instances[0]
        super(StaffBaseForm, self).__init__(*args, **kwargs)
        self.fields["instances"].choices = [] 
        self.fields["instances"].choices.append((0, "------"))
        if instances:
            for instance in instances:
                self.fields["instances"].choices.append((instance.id, instance.name))
    
    def clean_admin_email(self):
        user = User.objects.filter(email=self.cleaned_data["admin_email"])
        if len(user) != 0:
            raise forms.ValidationError("A user already exists with that email")
        else:
            return self.cleaned_data["admin_email"]
    
    def clean_admin_temp_pass_again(self):
        admin_temp_pass = self.cleaned_data["admin_temp_pass"]
        admin_temp_pass_again = self.cleaned_data["admin_temp_pass_again"]
        if (admin_temp_pass != admin_temp_pass_again):
            raise forms.ValidationError("The passwords do not match")
        else:
            return admin_temp_pass_again
    
    def clean_instances(self):
        instance_id = int(self.cleaned_data["instances"])
        if instance_id == 0:
            return None
        else:
            instance = Instance.objects.get(id=instance_id)
            return instance

class InstanceBaseForm(forms.Form):
    instance = forms.ModelChoiceField(required=False, queryset=Instance.objects.all())
    instance_name = forms.CharField(required=False, max_length=45)
   
class InstanceEditForm_org(forms.Form):
    name = forms.CharField(required=True, max_length=45)
    city = forms.CharField(required=False, max_length=255)
    state = forms.CharField(required=False, max_length=2)
    start_date = forms.DateTimeField(required=True)
    #This has to be named map, there can be only one and I am guessing it's a huge JS hack to make this work
    map = GoogleMapsField().formfield()
    days_for_mission = forms.IntegerField(required=True)
    
    def clean_map(self):
        map = self.cleaned_data.get('map')
        if not map:
            raise forms.ValidationError("The map doesn't exist")
        mapDict = simplejson.loads(map)
        if len(mapDict["markers"]) == 0:
            raise forms.ValidationError("Please select a point on the map")
        return map

class InstanceForm(TranslatableModelForm):

    class Meta:
        model = Instance
        exclude = ('language_code', 'location', 'name', 'description',)

    def __init__(self, *args, **kwargs):
        super(InstanceForm, self).__init__(*args, **kwargs)
        
        def _make_instance_trans_form(instance):
            lang = instance.language_code
            fields = {
                'name_'+lang : forms.CharField(max_length=45, initial=instance.name, label='Name'),
                'description_'+lang : forms.CharField(max_length=1000, initial=instance.description, label='Description'),
                'language_code_'+lang : forms.CharField(widget=forms.HiddenInput(), initial=instance.language_code, label='')
            }
            return type('InstanceTransForm', (forms.BaseForm,),
                    dict(
                         instance=instance,
                         prefix="instance_trans_"+instance.language_code+"_form",
                         base_fields = fields,
                    )
            )

        self.inner_trans_forms = []
        self.instance =  kwargs.get('instance')
        if self.instance:            
            for trans in self.instance.translations.all():
                #self.trans_forms[trans.language_code] = _make_instance_trans_form(instance=trans)()
                # Remove 'instance' from kwargs to pass the rest kwargs to trans_form
                if kwargs.has_key('instance'):
                    kwargs.pop('instance')
                trans_form = _make_instance_trans_form(instance=trans)(*args, **kwargs)
                trans_form_name = "instance_trans_" + trans.language_code + "_form"
                setattr(self, trans_form_name, trans_form)
                self.inner_trans_forms.append(trans_form)
                log.debug('created form:', trans_form_name)

        # go through the proxy model
        # because of custom instance formatting
        self.fields['curators'].queryset = CPIUser.objects.all()
        #self.fields['map'] = GoogleMapsField().formfield()

    def clean_map(self):
        map = self.cleaned_data.get('map')
        if not map:
            raise forms.ValidationError("The map doesn't exist")
        mapDict = simplejson.loads(map)
        if len(mapDict["markers"]) == 0:
            raise forms.ValidationError("Please select a point on the map")
        return map

    def is_valid(self):
        is_valid = super(InstanceForm, self).is_valid()
        if not is_valid:
            log.error("Error with form %s" % self.__class__.__name__)
            log.error(self.errors)
        is_valid_trans_forms = True

        for form in self.inner_trans_forms:
            if not form.is_valid():
                log.error("Error with form %s" % form.__class__.__name__)
                log.error(form.errors)
                is_valid_trans_forms = False

        log.debug((is_valid, is_valid_trans_forms))

        return is_valid and is_valid_trans_forms

    def save(self, *args, **kwargs):
        instance = super(InstanceForm, self).save(*args, **kwargs)

        for form in self.inner_trans_forms:
            new = form.instance.pk is None
            data = form.cleaned_data            
            trans_model = form.instance.__class__
            language_code = form.instance.language_code
            
            if not new:
                trans = get_cached_translation(instance)
                if not trans:
                    try:
                        trans = get_translation(instance, language_code)
                    except trans_model.DoesNotExist:
                        trans = trans_model()
            else:
                trans = trans_model()
                
            trans.name = data['name_%s' % language_code]
            trans.description = data['description_%s' % language_code]
            trans.language_code = language_code
            trans.master = instance
            trans.save()
            
        return instance

#class InstanceProcessForm(forms.Form):
#    process_name = forms.CharField(max_length=255)
#    process_description = forms.CharField(widget=forms.Textarea(attrs={"rows": 15, "cols": 160}))

class InstanceEmailForm(forms.Form):
    subject = forms.CharField()
    email = forms.CharField(widget=forms.Textarea(attrs={"rows": 6, "cols": 40}))

class ValueBaseForm(forms.Form):
    instances = forms.ChoiceField()
    
    def __init__(self, *args, **kwargs):
        initial =  kwargs.get("initial", {})
        instances = initial.get("instances", None)
        if instances:
            kwargs['initial']['instances'] = instances[0]
        super(ValueBaseForm, self).__init__(*args, **kwargs)
        self.fields["instances"].choices = []
        if instances:
            for instance in instances:
                self.fields["instances"].choices.append((instance.id, instance.name))

class MissionBaseForm(forms.Form):
    instances = forms.ChoiceField()
    
    def __init__(self, *args, **kwargs):
        initial =  kwargs.get("initial", {})
        instances = initial.get("instances", None)
        if instances:
            kwargs['initial']['instances'] = instances[0]
        super(MissionBaseForm, self).__init__(*args, **kwargs)
        self.fields["instances"].choices = []
        if instances:
            for instance in instances:
                self.fields["instances"].choices.append((instance.id, instance.name))

class ActivityBaseForm(forms.Form):
    instances = forms.ChoiceField()
    
    def __init__(self, *args, **kwargs):
        initial =  kwargs.get("initial", {})
        instances = initial.get("instances", None)
        if instances:
            kwargs['initial']['instances'] = instances[0]
        super(ActivityBaseForm, self).__init__(*args, **kwargs)
        self.fields["instances"].choices = []
        if instances:
            for instance in instances:
                self.fields["instances"].choices.append((instance.id, instance.name))
                
class ActivitySaveForm(forms.Form):
    missions = forms.ChoiceField(required=False)
    
    def __init__(self, *args, **kwargs):
        initial =  kwargs.get("initial", {})
        missions = initial.get("missions", None)
        if missions:
            kwargs['initial']['missions'] = missions[0]
        super(ActivitySaveForm, self).__init__(*args, **kwargs)
        self.fields["missions"].choices = []
        if missions:
            for mission in missions:
                self.fields["missions"].choices.append(mission)

class ActivityEditForm(forms.Form):
    name = forms.CharField()
    question = forms.CharField()
    instructions = forms.CharField(required=False)
    addInstructions = forms.CharField(required=False)
    points = forms.IntegerField(required=False)
    attachment = forms.ImageField(required=False)
    maxNumMarkers = forms.IntegerField(required=False)
    avatar = forms.FileField(required=False)
    bio = forms.CharField(required=False)
    
