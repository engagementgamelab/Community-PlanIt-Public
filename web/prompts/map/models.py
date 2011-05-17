from django.db import models
from django.contrib import admin

from gmapsfield.fields import GoogleMapsField
from web.prompts.models import Prompt

class MapPrompt(Prompt):
    map = GoogleMapsField()

    def save(self):
        self.prompt_type = "map"
        super(MapPrompt, self).save()

    class Meta:
        app_label = "prompts"
        verbose_name = "Map Prompt"
        verbose_name_plural = "Map Prompts"

class MapPromptAdmin(admin.ModelAdmin):
    exclude = ('download',)
