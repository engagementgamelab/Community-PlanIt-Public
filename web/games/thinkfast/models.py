from django.db import models
from django.contrib import admin
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

from web.games.models import Game
from web.prompts.basic.models import BasicPrompt
from web.responses.choices.models import ChoicesResponse

class ThinkFast(Game):
    prompt = models.ForeignKey(BasicPrompt, null=True, blank=True)
    response = models.ForeignKey(ChoicesResponse, null=True, blank=True)

#    object_id = models.PositiveIntegerField()
#    content_type = models.ForeignKey(ContentType)
#    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def save(self):
        self.game_type = "thinkfast"
        super(ThinkFast, self).save()

    class Meta:
        app_label = "games"
        verbose_name = "Think Fast! Game"
        verbose_name_plural = "Think Fast! Games"

    def __unicode__(self):
        return "Think Fast!"

class ThinkFastAdmin(admin.ModelAdmin):
    list_display = ('title', 'prompt', 'response',)

    #def queryset(self, request):
    #    qs = super(ThinkFastAdmin, self).queryset(request)
    #    return qs.filter(mission=request.session.get('mission'))
