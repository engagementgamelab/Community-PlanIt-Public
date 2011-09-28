from nani.forms import TranslatableModelForm
from nani.utils import get_translation

from gmapsfield.fields import GoogleMapsField

from django import forms
from django.conf import settings
from django.utils import simplejson

from instances.models import Instance
from values.models import Value
from player_activities.models import PlayerActivity
from missions.models import Mission
from accounts.models import CPIUser

import logging
from answers.models import Answer
from comments.forms import CommentForm
from django.forms.widgets import RadioSelect
from django.contrib.auth.models import User
log = logging.getLogger(__name__)


class TranslatableAdminBaseForm(TranslatableModelForm):

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance')
        languages = []
        if kwargs.has_key('languages'):
            languages = kwargs.pop('languages')
        super(TranslatableAdminBaseForm, self).__init__(instance=self.instance, *args, **kwargs)

        self.inner_trans_forms = []
        for language in languages:
            trans_model = self._meta.model._meta.translations_model
            try:
                trans = get_translation(self.instance, language.code)
            except trans_model.DoesNotExist:
                trans = trans_model()
            trans.language_code = language.code
            fields  = {}
            for field_name in self.instance._translated_field_names:
                if field_name in ['id', 'master', 'language_code']:
                    continue
                fields["".join([field_name, "_", language.code])] = forms.CharField(max_length=1000, 
                                                     initial=getattr(trans, field_name), 
                                                     label=field_name.capitalize()
                )
            fields['language_code_'+language.code] = forms.CharField(widget=forms.HiddenInput(), 
                                                                  initial=language.code, label='')
            trans_form =  type('AdminTransForm', (forms.BaseForm,),
                               dict(instance=trans,
                                    prefix="".join(["trans_", language.code, "_form"]),
                                    base_fields = fields,)
            )(*args, **kwargs)
            setattr(self, "".join(["trans_", language.code, "_form"]), trans_form)
            self.inner_trans_forms.append(trans_form)

    def is_valid(self):
        is_valid = super(TranslatableAdminBaseForm, self).is_valid()
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
        obj = super(TranslatableAdminBaseForm, self).save(*args, **kwargs)
        for form in self.inner_trans_forms:
            new = form.instance.pk is None
            cd = form.cleaned_data
            print cd
            trans_model = form.instance.__class__
            language_code = form.instance.language_code
            try:
                trans = get_translation(obj, language_code)
            except trans_model.DoesNotExist:
                trans = trans_model()

            for field_name in obj._translated_field_names:
                if field_name in ['id', 'master', 'language_code']:
                    continue
                setattr(trans, field_name, cd["".join([field_name, "_", language_code])])
            trans.language_code = language_code
            trans.master = obj
            trans.save()
        return obj


class InstanceForm(TranslatableAdminBaseForm):
    class Meta:
        model = Instance
        exclude = ('language_code', 'location', 'description',)

    def __init__(self, *args, **kwargs):
        # go through the proxy model
        # because of custom instance formatting
        #self.fields['curators'].queryset = CPIUser.objects.all()        
        super(InstanceForm, self).__init__(*args, **kwargs)
        self.fields['map'] = GoogleMapsField().formfield()

    def clean_map(self):
        map = self.cleaned_data.get('map')
        if not map:
            raise forms.ValidationError("The map doesn't exist")
        mapDict = simplejson.loads(map)
        if len(mapDict["markers"]) == 0:
            raise forms.ValidationError("Please select a point on the map")
        return map


class ValueForm(TranslatableAdminBaseForm):

    class Meta:
        model = Value
        exclude = ('language_code', 'message', 'instance', 'comments')


class ActivityForm(TranslatableAdminBaseForm):

    class Meta:
        model = PlayerActivity
        exclude = ('language_code', 'name', 'question', 'instructions', 'addInstructions', 
                   'creationUser', 'mission', 'createDate', 'attachment')


class MissionForm(TranslatableAdminBaseForm):

    class Meta:
        model = Mission
        exclude = ('language_code', 'start_date', 'end_date', 'name', 'description', 'instance', 'comments')


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        exclude = ('activity',)
        
        
class AdminCommentForm(CommentForm):    
    def __init__(self, instance=None, *args, **kwargs):
        super(AdminCommentForm, self).__init__(*args, **kwargs)
        self.fields['language'] = forms.ChoiceField(widget=RadioSelect, choices=settings.LANGUAGES)
        self.fields['user'] = forms.ModelChoiceField(queryset=User.objects.all())
        self.instance = instance        
        if instance is not None:
            self.fields['user'].initial = instance.user
            self.fields['language'].initial = instance.language_code
    

#####
# everything below is deprecated
class InstanceProcessForm(forms.Form):
    process_name = forms.CharField(max_length=255)
    process_description = forms.CharField(widget=forms.Textarea(attrs={"rows": 15, "cols": 160}))

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
                self.fields["instances"].choices.append((instance.id, instance.title))

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
    
