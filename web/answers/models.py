from django.template.defaultfilters import slugify
from django.db import models
from django.core.urlresolvers import reverse
from web.comments.models import Comment
from web.missions.models import Mission
from web.player_activities.models import (PlayerActivity, MultiChoiceActivity, 
        PlayerEmpathyActivity, PlayerMapActivity)
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from gmapsfield.fields import GoogleMapsField

import datetime

__all__ = (
        'Answer', 'AnswerSingleResponse', 'AnswerOpenEnded', 'AnswerMap', 'AnswerEmpathy', 'AnswerMultiChoice'
)

class Answer(models.Model):
    answerUser = models.ForeignKey(User, editable=False, related_name='answers')
    comments = generic.GenericRelation(Comment)
    createDate = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        self.createDate = datetime.datetime.now()
        super(Answer, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ("player_activities:overview", [self.activity.id])

class AnswerOpenEnded(Answer):
    comment = models.TextField()
    activity = models.ForeignKey(PlayerActivity, related_name='openended_answers')

class AnswerSingleResponse(Answer):
    selected = models.ForeignKey(MultiChoiceActivity, related_name='singleresponse_answers')
    activity = models.ForeignKey(PlayerActivity, related_name='singleresponse_answers')

#This is nasty but it's the simple way to get many checked values
#for the user stored
class AnswerMultiChoice(models.Model):
    user = models.ForeignKey(User)
    option = models.ForeignKey(MultiChoiceActivity, related_name='multiresponse_answers')
    comments = generic.GenericRelation(Comment)

    def __unicode__(self):
        return self.option.value

    @models.permalink
    def get_absolute_url(self):
        return ("player_activities:overview", [self.option.activity.id])

class AnswerMap(Answer):
    map = GoogleMapsField()
    activity = models.ForeignKey(PlayerMapActivity, related_name='map_answers')

class AnswerEmpathy(Answer):
    activity = models.ForeignKey(PlayerEmpathyActivity, related_name='empathy_answers')

