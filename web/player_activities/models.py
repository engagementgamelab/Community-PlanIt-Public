import datetime

from django.db import models
from django.template.defaultfilters import slugify

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from nani.models import TranslatableModel, TranslatedFields

from web.accounts.models import determine_path
from web.attachments.models import Attachment
from web.missions.models import Mission

class PlayerActivityType(models.Model):
    type = models.CharField(max_length=255)
    displayType = models.CharField(max_length=255)
    defaultPoints = models.IntegerField(default=10)

    def __unicode__(self):
        return self.type
    
class PlayerActivity(TranslatableModel):
    slug = models.SlugField(editable=False)
    creationUser = models.ForeignKey(User)
    mission = models.ForeignKey(Mission, related_name='activities')
    type = models.ForeignKey(PlayerActivityType)
    createDate = models.DateTimeField(editable=False)
    points = models.IntegerField(blank=True, null=True, default=None)
    attachment = models.ManyToManyField(Attachment, blank=True, null=True)

    translations = TranslatedFields(
        name = models.CharField(max_length=255),
        question = models.CharField(max_length=1000),
        instructions = models.CharField(max_length=255, null=True, blank=True),
        addInstructions = models.CharField(max_length=255, null=True, blank=True),
        meta = {'ordering': ['name',],
        },
    )

    class Meta:
        verbose_name_plural = 'Player Activities'
        #removing contraint since name is now translated
        #and it seems you cannot mix translated fields
        #unique_together = ('mission', 'type')
    
    def __unicode__(self):
        return self.safe_translation_getter('name', 'Activity: %s' % self.pk)

    def save(self):
        self.slug = slugify(self.pk)
        self.createDate = datetime.datetime.now()
        super(PlayerActivity, self).save()
    
    def getPoints(self):
        if self.points == None:
            return self.type.defaultPoints
        else:
            return self.points

class PlayerMapActivity(PlayerActivity):
    maxNumMarkers = models.IntegerField(default=5)
    #django-nani complains that no translated fields exist on a sublclass of TraslatableModel
    translations = TranslatedFields(
        tbd = models.CharField(max_length=10),
    )
    
    def save(self):
        self.slug = slugify(self.pk)
        self.createDate = datetime.datetime.now()
        self.type = PlayerActivityType.objects.get(type="map")
        super(PlayerMapActivity, self).save()

class PlayerEmpathyActivity(PlayerActivity):
    avatar = models.ImageField(upload_to=determine_path, null=True, blank=True)
    translations = TranslatedFields(
        bio = models.CharField(max_length=1000),
    )
    
    def save(self):
        self.slug = slugify(self.name)
        self.createDate = datetime.datetime.now()
        self.type = PlayerActivityType.objects.get(type="empathy")
        super(PlayerEmpathyActivity, self).save()

class MultiChoiceActivity(TranslatableModel):
    activity = models.ForeignKey(PlayerActivity)

    translations = TranslatedFields(
        value = models.CharField(max_length=255),
    )

class PlayerActivityTypeAdmin(admin.ModelAdmin):
    list_display = ('type', 'defaultPoints',)

class PlayerActivityAdmin(admin.ModelAdmin):
    list_display = ('creationUser', 'mission', 'type', 'createDate', 'points') #excluding translated fields 'name', 'question', 
    
