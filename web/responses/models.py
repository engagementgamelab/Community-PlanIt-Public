from django.db import models

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic

from attachments_v2.models import Attachment
from comments.models import Comment

class Response(models.Model):
    response_type = models.CharField(max_length=45, editable=False)
    flagged = models.IntegerField(default=0)
    answer = models.BooleanField(default=False, editable=False)

    attachment = models.ManyToManyField(Attachment, blank=True, null=True)
    comments = generic.GenericRelation(Comment)
