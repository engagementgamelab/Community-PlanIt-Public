from django.template.defaultfilters import slugify
from django.db import models
from web.responses.models import Response
from web.comments.models import Comment
from web.missions.models import Mission
from web.player_activities.models import PlayerActivity
from web.accounts.models import determine_path
from django.contrib.auth.models import User
from gmapsfield.fields import GoogleMapsField

#valid types are:
# open_ended, single_response, map, empathy, multi_reponse
class AnswerType(models.Model):
    type = models.CharField(max_length=255)
    defaultPoints = models.IntegerField(deafult=10)
    points = models.IntegerField(blank=True, null=True, default=None)
    
class Answer(models.Model):
    #TODO: This might benefit from a 1:1 relationship
    activity = models.ForeignKey(PlayerActivity)
    type = models.ForeignKey(AnswerType)
    instructions = models.CharField(max_length=255)
    addInstructions = models.CharField(max_length=255)
    answerUser = models.ForeignKey(User)

class MultiChoiceOption(models.Model):
    answer = models.ForeignKey(Answer)
    value = models.CharField(max_length=255)

class AnswerOpenEnded(Answer):
    answerbox = models.TextField()
    
    def save(self):
        self.type = AnswerType.objects.get_or_create(type="open_ended")
        super(Answer, self).save()
    
class AnswerSingleResponse(Answer):
    selected = models.ForeignKey(MultiChoiceOption)
    
    def save(self):
        self.type = AnswerType.objects.get_or_create(type="single_response")
        super(Answer, self).save()
        
class AnswerMap(Answer):
    map = GoogleMapsField()
    answerBox = models.TextField(blank=True, null=True)
    maxNumMarkers = models.IntegerField(default=5)

    def save(self):
        self.type = AnswerType.objects.get_or_create(type="map")
        super(Answer, self).save()
            
class AnswerEmpathy(Answer):
    avatar = models.ImageField(upload_to=determine_path, null=True, blank=True)
    bio = models.CharField(max_length = 255)
    answerBox = models.TextField()
    
    def save(self):
        self.type = AnswerType.objects.get_or_create(type="empathy")
        super(Answer, self).save()
        
#This is nasty but it's the simple way to get many checked values
#for the user stored
class AnswerMultiChoice(models.Model):
    user = models.ForeignKey(User)
    option = models.ForeignKey(MultiChoiceOption)

    def save(self):
        self.type = AnswerType.objects.get_or_create(type="multi_reponse")
        super(Answer, self).save()
