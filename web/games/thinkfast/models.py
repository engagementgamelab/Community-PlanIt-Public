from django.db import models
from django.contrib import admin
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

from web.games.models import Game
from web.prompts.basic.models import BasicPrompt

class ThinkFast(Game):
    def save(self):
        self.game_type = "thinkfast"
        super(ThinkFast, self).save()

    def __unicode__(self):
        return "Think Fast!"

class ThinkFastAdmin(admin.ModelAdmin):
    list_display = ('title', 'prompt',)
