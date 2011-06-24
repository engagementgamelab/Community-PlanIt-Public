from django.template.defaultfilters import slugify
from django.db import models
from web.attachments.models import Attachment
from web.missions.models import Mission
from django.contrib.auth.models import User
import datetime

#from django.contrib.auth.models import User
class PlayerActivity(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(editable=False)
    question = models.CharField(max_length=1000)
    creationUser = models.ForeignKey(User)
    misison = models.ForeignKey(Mission)
    createDate = models.DateTimeField(editable=False)
    attachment = models.ManyToManyField(Attachment, blank=True, null=True)
    
    def save(self):
        slug = slugify(self.name)
        createDate = datetime.datetime.now()
        super(PlayerActivity, self).save()
    
    