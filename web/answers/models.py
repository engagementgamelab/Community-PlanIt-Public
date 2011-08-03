from django.template.defaultfilters import slugify
from django.db import models
from web.responses.models import Response
from web.comments.models import Comment
from web.missions.models import Mission
from web.player_activities.models import PlayerActivity, MultiChoiceActivity
from django.contrib.auth.models import User
from gmapsfield.fields import GoogleMapsField

class Answer(models.Model):
    #TODO: This might benefit from a 1:1 relationship
    activity = models.ForeignKey(PlayerActivity, related_name='answers')
    answerUser = models.ForeignKey(User, related_name='answers')

class AnswerOpenEnded(Answer):
    answerBox = models.CharField(max_length=1000)
    
class AnswerSingleResponse(Answer):
    selected = models.ForeignKey(MultiChoiceActivity)

class AnswerMap(Answer):
    answerBox = models.CharField(max_length=1000, blank=True, null=True)
    map = GoogleMapsField()
    
class AnswerEmpathy(Answer):
    answerBox = models.CharField(max_length=1000)
        
#This is nasty but it's the simple way to get many checked values
#for the user stored
class AnswerMultiChoice(models.Model):
    user = models.ForeignKey(User)
    option = models.ForeignKey(MultiChoiceActivity)
