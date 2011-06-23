from django.template.defaultfilters import slugify
from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from web.prompts.models import Prompt
from web.responses.models import Response
from web.comments.models import Comment
from web.missions.models import Mission

from django.contrib.auth.models import User

# Base Game
#TODO: Make a foreign key to missions, currently requires a mission slug
class Game(models.Model):
    game_type = models.CharField(max_length=45, editable=False)
    title = models.CharField(max_length=45)
    slug = models.SlugField(editable=False)
    active = models.BooleanField(editable=False,default=True)
    mission = models.ForeignKey(Mission)
    comments = models.ManyToManyField(Comment, blank=True, null=True)

    def save(self):
        self.slug = slugify(self.title)
        super(Game, self).save()

    def __unicode__(self):
        label = self.game_type +": "+ self.title
        return label[:25]

class PlayerGame(models.Model):
    visible = models.BooleanField(default=True)
    completed = models.BooleanField(default=False)

    game = models.ForeignKey(Game)
    user = models.ForeignKey(User)

    comments = models.ManyToManyField(Comment, blank=True, null=True)

# Import games
from web.games.othershoes.models import *
from web.games.thinkfast.models import *
from web.games.mapit.models import *
