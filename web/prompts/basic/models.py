from django.db import models
from django.contrib import admin

from web.prompts.models import Prompt

class BasicPrompt(Prompt):
    message = models.CharField(max_length=260)

    game = models.ForeignKey('games.Game', related_name='basicprompt_game', null=True, blank=True)

    def save(self):
        self.prompt_type = "basic"
        super(BasicPrompt, self).save()

    class Meta:
        app_label = "prompts"
        verbose_name = "Basic Prompt"
        verbose_name_plural = "Basic Prompts"

    def render(self):
        return self.message

    def __unicode__(self):
        return self.message[:25]

class BasicPromptAdmin(admin.ModelAdmin):
    exclude = ('game','download')
