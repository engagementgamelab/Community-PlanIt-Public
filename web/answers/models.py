from django.template.defaultfilters import slugify
from django.db import models
from web.comments.models import Comment
from web.missions.models import Mission
from web.player_activities.models import PlayerActivity, MultiChoiceActivity
from django.contrib.auth.models import User
from gmapsfield.fields import GoogleMapsField

import datetime

class Answer(models.Model):
    #TODO: This might benefit from a 1:1 relationship
    activity = models.ForeignKey(PlayerActivity, related_name='answers')
    answerUser = models.ForeignKey(User, related_name='answers')
    comment = models.ForeignKey(Comment, null=True, blank=True)
    createDate = models.DateTimeField()
    
    def save(self):
        self.createDate = datetime.datetime.now()
        super(Answer, self).save()
        
#class AnswerOpenEnded(Answer):
#    comment = models.ForeignKey(Comment)
    
class AnswerSingleResponse(Answer):
    selected = models.ForeignKey(MultiChoiceActivity)

class AnswerMap(Answer):
    map = GoogleMapsField()
    
#class AnswerEmpathy(Answer):
#    answerBox = models.CharField(max_length=1000)
        
#This is nasty but it's the simple way to get many checked values
#for the user stored
class AnswerMultiChoice(models.Model):
    user = models.ForeignKey(User)
    option = models.ForeignKey(MultiChoiceActivity)
    comment = models.ForeignKey(Comment, null=True, blank=True)
