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
    activity = models.ForeignKey(PlayerActivity)
    instructions = models.CharField(max_length=255)
    addInstructions = models.CharField(max_length=255)
    answerUser = models.ForeignKey(User)

class AnswerOpenEnded(Answer):
    answerbox = models.CharField(max_length=1000)
    
    def save(self):
        self.type = AnswerType.objects.get_or_create(type="open_ended")
        super(Answer, self).save()
    
class AnswerSingleResponse(Answer):
    selected = models.ForeignKey(MultiChoiceActivity)
    
    def save(self):
        self.type = AnswerType.objects.get_or_create(type="single_response")
        super(Answer, self).save()
        
class AnswerMap(Answer):
    answerBox = models.TextField(blank=True, null=True)
    maxNumMarkers = models.IntegerField(default=5)

    def save(self):
        self.type = AnswerType.objects.get_or_create(type="map")
        super(Answer, self).save()

class UserMapPoints(models.Model):
    user = models.ForeignKey(User)
    map = models.ForeignKey(AnswerMap)
    point = GoogleMapsField()

class AnswerEmpathy(Answer):
    answerBox = models.TextField()
    
    def save(self):
        self.type = AnswerType.objects.get_or_create(type="empathy")
        super(Answer, self).save()
        
#This is nasty but it's the simple way to get many checked values
#for the user stored
class AnswerMultiChoice(models.Model):
    user = models.ForeignKey(User)
    option = models.ForeignKey(MultiChoiceActivity)

    def save(self):
        self.type = AnswerType.objects.get_or_create(type="multi_reponse")
        super(Answer, self).save()
