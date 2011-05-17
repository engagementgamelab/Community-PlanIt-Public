from web.attachments.models import Attachment
from django.contrib import admin
from django.db import models

class Prompt(models.Model):
    prompt_type = models.CharField(max_length=45, editable=False)
    download = models.ForeignKey(Attachment, blank=True, null=True, related_name="get_prompt_download")

    attachments = models.ManyToManyField(Attachment, blank=True)

from web.prompts.basic.models import *
from web.prompts.map.models import *
from web.prompts.profile.models import *
