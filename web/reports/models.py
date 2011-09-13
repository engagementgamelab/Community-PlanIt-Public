import datetime

from django.db import models

from django.contrib import admin
from django.contrib.auth.models import User

from gmapsfield.fields import GoogleMapsField
from localeurl.utils import locale_url
from localeurl.templatetags.localeurl_tags import rmlocale

from instances.models import Instance
from django.utils import translation

class Activity(models.Model):
    action = models.CharField(max_length=48)
    data = models.TextField()
    url = models.URLField(blank=True, null=True)
    location = GoogleMapsField(blank=True, null=True) # Make editable false
    date = models.DateTimeField(default=datetime.datetime.now)
    type = models.CharField(max_length=255)

    user = models.ForeignKey(User, blank=True, null=True)
    instance = models.ForeignKey(Instance, blank=True, null=True, editable=False)
    
    class Meta:
        verbose_name = 'Activity'
        verbose_name_plural = 'Activities'

    def __unicode__(self):
        label = self.action +' - '+ self.data
        return label
    
    def get_url(self):
        if self.url:            
            url = rmlocale(self.url)            
            return locale_url(url, translation.get_language())
        return None
