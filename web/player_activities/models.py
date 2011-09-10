import datetime

from nani.admin import TranslatableAdmin, TranslatableStackedInline
from nani.models import TranslatableModel, TranslatedFields

from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from web.accounts.models import determine_path
from web.attachments.models import Attachment
from web.missions.models import Mission
from django.contrib.admin.options import ModelAdmin

__all__ = ( 'PlayerActivityType','PlayerActivity', 'PlayerMapActivity', 'PlayerEmpathyActivity', 'MultiChoiceActivity', )

def determine_path(instance, filename):
    return 'uploads/'+ str(instance.creationUser.id) +'/'+ filename

class PlayerActivityType(models.Model):
    type = models.CharField(max_length=255)
    displayType = models.CharField(max_length=255)
    defaultPoints = models.IntegerField(default=10)

    class Meta:
        verbose_name_plural = 'Player Activity Types'

    def __unicode__(self):
        return self.type

class PlayerActivityBase(TranslatableModel):

    slug = models.SlugField(editable=False)
    creationUser = models.ForeignKey(User, verbose_name="created by")
    mission = models.ForeignKey(Mission, related_name='%(app_label)s_%(class)s_related')
    type = models.ForeignKey(PlayerActivityType)
    createDate = models.DateTimeField(editable=False)
    points = models.IntegerField(blank=True, null=True, default=None)
    attachment = models.ManyToManyField(Attachment, blank=True, null=True)

    class Meta:
        abstract = True

    def admin_name(self):
        return self.__unicode__()
    admin_name.short_description = 'Name'

class PlayerActivity(PlayerActivityBase):

    translations = TranslatedFields(
        name = models.CharField(max_length=255),
        question = models.CharField(max_length=1000),
        instructions = models.CharField(max_length=255, null=True, blank=True),
        addInstructions = models.CharField(max_length=255, null=True, blank=True),
        meta = {'ordering': ['name']},
    )

    class Meta:
        verbose_name_plural = 'Player Activities'

    def __unicode__(self):
        return self.safe_translation_getter('name', '%s' % self.pk)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.pk)
        self.createDate = datetime.datetime.now()
        super(PlayerActivity, self).save(*args, **kwargs)

    def getPoints(self):
        if self.points == None:
            return self.type.defaultPoints
        else:
            return self.points

class PlayerMapActivity(PlayerActivityBase):
    maxNumMarkers = models.IntegerField(default=5)
    #django-nani complains that no translated fields exist on a sublclass of TraslatableModel

    translations = TranslatedFields(
        name = models.CharField(max_length=255),
        question = models.CharField(max_length=1000),
        instructions = models.CharField(max_length=255, null=True, blank=True),
        addInstructions = models.CharField(max_length=255, null=True, blank=True),
        meta = {'ordering': ['name']},
    )
    
    class Meta:
        verbose_name_plural = 'Player Map Activities'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.pk)
        self.createDate = datetime.datetime.now()
        self.type = PlayerActivityType.objects.get(type="map")
        super(PlayerMapActivity, self).save(*args, **kwargs)

class PlayerEmpathyActivity(PlayerActivityBase):
    avatar = models.ImageField(upload_to=determine_path, null=True, blank=True)
    translations = TranslatedFields(        
        bio = models.TextField(max_length=1000),
        name = models.CharField(max_length=255),
        question = models.CharField(max_length=1000),
        instructions = models.CharField(max_length=255, null=True, blank=True),
        addInstructions = models.CharField(max_length=255, null=True, blank=True),
    )
    
    class Meta:
        verbose_name_plural = 'Player Empathy Activities'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.pk)
        self.createDate = datetime.datetime.now()
        self.type = PlayerActivityType.objects.get(type="empathy")
        super(PlayerEmpathyActivity, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.safe_translation_getter('value', '%s' % self.bio[:10])

class MultiChoiceActivity(TranslatableModel):
    activity = models.ForeignKey(PlayerActivity)

    translations = TranslatedFields(
        value = models.CharField(max_length=255),
    )

    class Meta:
        verbose_name = 'Multiple Choice Activity'
        verbose_name_plural = 'Multiple Choice Activities'

    def __unicode__(self):
        return self.safe_translation_getter('value', '%s' % self.pk)

    def admin_name(self):
        return self.__unicode__()
    admin_name.short_description = 'Name'

#*******************
#### admin =========

class PlayerActivityTypeAdmin(ModelAdmin):
    list_display = ('type', 'defaultPoints',)


class MultipleChoiceActivityInline(TranslatableStackedInline):
	model = MultiChoiceActivity


class PlayerActivityAdmin(TranslatableAdmin):
    list_display = ('admin_name', 'mission', 'type', 'all_translations')

    inlines = [
            MultipleChoiceActivityInline,
    ]
    #list_display = ('creationUser', 'mission', 'type', 'createDate', 'points')
    #'question', 
    #'name', 

    #fieldsets = (
    #    (None, {
    #        'fields': ('name', 'question', 'instructions', 'addInstructions')
    #    }),
        #('Advanced options', {
        #    'classes': ('collapse',),
        #    'fields': ('enable_comments', 'registration_required', 'template_name')
        #}),
    #)



class PlayerEmpathyActivityAdmin(TranslatableAdmin):
    list_display = ('admin_name', 'mission', 'type')

class MultiChoiceActivityAdmin(TranslatableAdmin):
    list_display = ('admin_name',)
    
class PlayerMapActivityAdmin(TranslatableAdmin):
    list_display = ('admin_name', 'mission', 'type')
