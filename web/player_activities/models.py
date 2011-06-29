from django.template.defaultfilters import slugify
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from web.attachments.models import Attachment
from web.missions.models import Mission
from web.accounts.models import determine_path
import datetime

#from django.contrib.auth.models import User

#valid types are:
# open_ended, single_response, map, empathy, multi_reponse
class PlayerActivityType(models.Model):
    type = models.CharField(max_length=255)
    defaultPoints = models.IntegerField(default=10)
    
    
class PlayerActivity(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(editable=False)
    question = models.CharField(max_length=1000)
    creationUser = models.ForeignKey(User)
    mission = models.ForeignKey(Mission)
    type = models.ForeignKey(PlayerActivityType)
    createDate = models.DateTimeField(editable=False)
    attachment = models.ManyToManyField(Attachment, blank=True, null=True)
    avatar = models.ImageField(upload_to=determine_path, null=True, blank=True)
    bio = models.CharField(max_length=255, null=True, blank=True)
    points = models.IntegerField(blank=True, null=True, default=None)
    
    def save(self):
        self.slug = slugify(self.name)
        self.createDate = datetime.datetime.now()
        super(PlayerActivity, self).save()
    
    def getPoints(self):
        if self.points == None:
            return self.type.defaultPoints
        else:
            return self.points

class MultiChoiceActivity(models.Model):
    activity = models.ForeignKey(PlayerActivity)
    value = models.CharField(max_length=255)

class PlayerActivityTypeAdmin(admin.ModelAdmin):
    list_display = ('type', 'defaultPoints',)

class PlayerActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'question', 'creationUser', 'mission', 'type', 'createDate', 'points')
    