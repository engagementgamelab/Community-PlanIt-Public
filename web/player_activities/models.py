import datetime

from django.db import models
from django.template.defaultfilters import slugify

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from web.attachments.models import Attachment
from web.missions.models import Mission

def determine_path(instance, filename):
    return 'uploads/'+ str(instance.creationUser.id) +'/'+ filename

class PlayerActivityType(models.Model):
    type = models.CharField(max_length=255)
    displayType = models.CharField(max_length=255)
    defaultPoints = models.IntegerField(default=10)

    def __unicode__(self):
        return self.type
    
class PlayerActivity(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(editable=False)
    question = models.CharField(max_length=1000)
    creationUser = models.ForeignKey(User)
    mission = models.ForeignKey(Mission, related_name='activities')
    type = models.ForeignKey(PlayerActivityType)
    createDate = models.DateTimeField(editable=False)
    instructions = models.CharField(max_length=255, null=True, blank=True)
    addInstructions = models.CharField(max_length=255, null=True, blank=True)
    points = models.IntegerField(blank=True, null=True, default=None)
    attachment = models.ManyToManyField(Attachment, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Player Activities'
        unique_together = ('name', 'mission', 'type')
        ordering = ('name',)
    
    def __unicode__(self):
        return self.name

    def save(self):
        self.slug = slugify(self.name)
        self.createDate = datetime.datetime.now()
        super(PlayerActivity, self).save()
    
    def getPoints(self):
        if self.points == None:
            return self.type.defaultPoints
        else:
            return self.points

class PlayerMapActivity(PlayerActivity):
    maxNumMarkers = models.IntegerField(default=5)
    
    def save(self):
        self.slug = slugify(self.name)
        self.createDate = datetime.datetime.now()
        self.type = PlayerActivityType.objects.get(type="map")
        super(PlayerMapActivity, self).save()

class PlayerEmpathyActivity(PlayerActivity):
    avatar = models.ImageField(upload_to=determine_path, null=True, blank=True)
    bio = models.CharField(max_length=1000)
    
    def save(self):
        self.slug = slugify(self.name)
        self.createDate = datetime.datetime.now()
        self.type = PlayerActivityType.objects.get(type="empathy")
        super(PlayerEmpathyActivity, self).save()

class MultiChoiceActivity(models.Model):
    activity = models.ForeignKey(PlayerActivity)
    value = models.CharField(max_length=255)

class PlayerActivityTypeAdmin(admin.ModelAdmin):
    list_display = ('type', 'defaultPoints',)

class PlayerActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'question', 'creationUser', 'mission', 'type', 'createDate', 'points')
    
