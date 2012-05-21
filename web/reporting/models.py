import os.path
import datetime

from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import filesizeformat

from web.instances.models import Instance

def determine_path(instance, filename):
    return os.path.join('uploads/reports', str(instance.instance.pk), filename)

class Report(models.Model):

    title = models.CharField(max_length=255, blank=True, default='')
    file = models.FileField(upload_to=determine_path, blank=True, null=True)
    instance = models.ForeignKey(Instance, blank=True, null=True)
    user = models.ForeignKey(User, blank=True, null=True, editable=False)
    db_queries = models.IntegerField(default=0)
    time_to_run = models.IntegerField(default=0)
    date_added = models.DateTimeField(default=datetime.datetime.now, editable=False)

    @property
    def filesize(self):
        try:
            return filesizeformat(self.file.size)
        except:
            return '-'

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ('-date_added',)
