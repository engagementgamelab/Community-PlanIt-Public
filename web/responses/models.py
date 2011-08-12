from django.db import models
from django.contrib import admin

from web.comments.models import Comment
from web.attachments.models import Attachment
from django.contrib.auth.models import User

class Response(models.Model):
    response_type = models.CharField(max_length=45, editable=False)
    flagged = models.IntegerField(default=0)
    answer = models.BooleanField(default=False, editable=False)

    attachment = models.ManyToManyField(Attachment, blank=True, null=True)
    comments = models.ManyToManyField(Comment, blank=True)
