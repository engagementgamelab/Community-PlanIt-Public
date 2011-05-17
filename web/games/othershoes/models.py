from django.db import models
from django.contrib import admin
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

from web.games.models import Game
from web.prompts.profile.models import ProfilePrompt
from web.responses.comment.models import CommentResponse

class OtherShoes(Game):
    prompt = models.ForeignKey(ProfilePrompt, null=True, blank=True)
    response = models.ForeignKey(CommentResponse, null=True, blank=True)

#    object_id = models.PositiveIntegerField()
#    content_type = models.ForeignKey(ContentType)
#    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def save(self):
        self.game_type = "othershoes"
        super(OtherShoes, self).save()

    class Meta:
        app_label = "games"
        verbose_name = "Other Shoes Game"
        verbose_name_plural = "Other Shoes Games"

    def __unicode__(self):
        return "Other Shoes"

class OtherShoesAdmin(admin.ModelAdmin):
    list_display = ('title', 'prompt', 'response',)

    #def queryset(self, request):
    #    qs = super(OtherShoesAdmin, self).queryset(request)
    #    return qs.filter(mission=request.session.get('mission'))
