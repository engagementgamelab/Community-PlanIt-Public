from django.template.defaultfilters import slugify
from django.db import models
from web.attachments.models import Attachment
from web.missions.models import Mission
from django.contrib import admin
from django.contrib.auth.models import User
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
    misison = models.ForeignKey(Mission)
    type = models.ForeignKey(PlayerActivityType)
    createDate = models.DateTimeField(editable=False)
    attachment = models.ManyToManyField(Attachment, blank=True, null=True)
    points = models.IntegerField(blank=True, null=True, default=None)
    
    def save(self):
        self.slug = slugify(self.name)
        self.createDate = datetime.datetime.now()
        super(PlayerActivity, self).save()
    
    def getPoints(self):
        if points == None:
            return type.defaultPoints
        else:
            return points

class PlayerActivityTypeAdmin(admin.ModelAdmin):
    list_display = ('type', 'defaultPoints',)

class PlayerActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'question', 'creationUser', 'misison', 'type', 'createDate', 'points')
    