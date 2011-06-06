from django.db import models
from django.contrib import admin
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

from web.games.models import Game
from web.prompts.profile.models import ProfilePrompt
from web.comments.models import Comment
from web.responses.comment.models import CommentResponse

class OtherShoes(Game):
    prompt = models.ForeignKey(ProfilePrompt, null=True, blank=True)

    # the discussion captured in 'comments' replaces the mutable
    # CommentResponse answers, which could be changed, trashing entire
    # discussions
    comments = models.ManyToManyField(Comment, blank=True, null=True)

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
    list_display = ('title', 'prompt')
