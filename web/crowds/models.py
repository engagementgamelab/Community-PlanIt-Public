import os.path
import datetime

from stream import utils as stream_utils
from gmapsfield.fields import GoogleMapsField

from django.conf import settings
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic

from attachments.models import Attachment
from comments.models import Comment
from instances.models import Instance
from responses.comment.models import CommentResponse

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^gmapsfield\.fields\.GoogleMapsField"])

class CrowdManager(models.Manager):

    def upcoming(self):
        now = datetime.datetime.now()
        return self.filter(start_date__gte=now).order_by('start_date')

    def past(self):
        now = datetime.datetime.now()
        return self.filter(end_date__lt=now).order_by('start_date')

def determine_path(instance, filename):
    return os.path.join('uploads/crowds/', str(instance.creator.id), filename)

class Crowd(models.Model):
    name = models.CharField(max_length=255)
    map = GoogleMapsField()
    image = models.ImageField(upload_to=determine_path, null=True, blank=True)

    description = models.TextField()
    confirmation_code = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    flagged = models.BooleanField(default=0, editable=False)

    instance = models.ForeignKey(Instance, related_name='crowds')
    creator = models.ForeignKey(User, related_name='my_created_crowds')
    participants = models.ManyToManyField(User, blank=True, related_name='my_participating_crowds')
    attachments = models.ManyToManyField(Attachment, blank=True)
    comments = generic.GenericRelation(Comment)

    objects = CrowdManager()

    class Meta:
        ordering = ['start_date']

    @models.permalink
    def get_absolute_url(self):
        return ('crowds:crowd', [str(self.id)])

    @property
    def stream_action_title(self):
        return self.name

    def is_active(self):
        if not self.start_date:
            return True
        now = datetime.datetime.now()
        return self.start_date <= now and now <= self.end_date

    def is_expired(self):
        return self.end_date is not None and datetime.datetime.now() > self.end_date

    def is_started(self):
        return self.start_date is None or datetime.datetime.now() >= self.start_date

    def __unicode__(self):
        return self.name

#stream_utils.register_action_object(Crowd)
#stream_utils.register_target(Crowd)

