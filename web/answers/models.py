from django.template.defaultfilters import slugify
from django.db import models
from web.responses.models import Response
from web.comments.models import Comment
from web.missions.models import Mission
from web.activities.models import Activity
from web.accounts.models import determine_path
from django.contrib.auth.models import User
from gmapsfield.fields import GoogleMapsField


class AnswerType(models.Model):
    type = models.CharField(max_length=255)
    defaultPoints = models.IntegerField()
    
class Answer(models.Model):
    #TODO: This might benefit from a 1:1 relationship
    activity = models.ForeignKey(Activity)
    type = models.ForeignKey(AnswerType)
    instructions = models.CharField(max_length=255)
    addInstructions = models.CharField(max_length=255)
    answerUser = models.ForeignKey(User)

class MultiChoiceOption(models.Model):
    answer = models.ForeignKey(Answer)
    value = models.CharField(max_length=255)

class AnswerOpenEnded(Answer):
    answerbox = models.TextField()
    
class AnswerSingleResponse(Answer):
    selected = models.ForeignKey(MultiChoiceOption)

class AnswerMap(Answer):
    map = GoogleMapsField()
    answerBox = models.TextField(blank=True, null=True)
    maxNumMarkers = models.IntegerField(default=5)
    
class AnswerEmpathy(Answer):
    avatar = models.ImageField(upload_to=determine_path, null=True, blank=True)
    bio = models.CharField(max_length = 255)
    answerBox = models.TextField()
    
#This is nasty but it's the simple way to get many checked values
#for the user stored
class AnswerMultiChoice(models.Model):
    user = models.ForeignKey(User)
    option = models.ForeignKey(MultiChoiceOption)
    
