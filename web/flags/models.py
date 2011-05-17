from django.contrib.auth.models import User
from django.db import models

class PlayerFlag(models.Model):
    app = models.CharField(max_length=255)
    app_id = models.CharField(max_length=255)
    label = models.CharField(max_length=255)
    
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.label[:25] or 'None'
