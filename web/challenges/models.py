import datetime
from web.instances.models import Instance
from web.attachments.models import Attachment
from web.comments.models import Comment
from web.responses.models import Response
from web.responses.comment.models import CommentResponse
from gmapsfield.fields import GoogleMapsField
from django.contrib.auth.models import User
from django.db import models
from django.contrib import admin

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^gmapsfield\.fields\.GoogleMapsField"])

class QuerySetManager(models.Manager):
    def get_query_set(self):
        return self.model.QuerySet(self.model)

#Create the base model for the view
#This is where all of the data lies.
class Challenge(models.Model):
    map = GoogleMapsField()
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    flagged = models.BooleanField(default=0, editable=False)

    instance = models.ForeignKey(Instance)
    user = models.ForeignKey(User, editable=False)
    attachments = models.ManyToManyField(Attachment, blank=True)
    comments = models.ManyToManyField(Comment, blank=True)
    game_type = models.CharField(max_length=45, editable=False)
    
    def is_active(self):
        if datetime.datetime.now() >= self.start_date and datetime.datetime.now() <= self.end_date:
            return True;
        else:
            return False;
        
    def is_expired(self):
        if datetime.datetime.now() >= self.end_date:
            return True
        else:
            return False
    
    def is_started(self):
        if datetime.datetime.now() >= self.start_date:
            return True
        else:
            return False
    
    def save(self):
        self.game_type = "challenge"
        #TODO: Make sure this is correct, the None map I am not sure about - BMH
        if self.map == "None":
            self.map = self.instance.location
        super(Challenge, self).save()

    # Faking out the objects collection to pull from the inner model
    # class.
    objects = QuerySetManager()

    class QuerySet(models.query.QuerySet):
        def active(self):
            return self.filter(start_date__lt=datetime.datetime.now()).filter(end_date__gt=datetime.datetime.now()).order_by('end_date')

    def __unicode__(self):
        label = self.name or 'None'
        return label[:25]

class ChallengeAdmin(admin.ModelAdmin):
    def queryset(self, request):
        qs = super(ChallengeAdmin, self).queryset(request)
        return qs.filter(instance=request.session.get('admin_instance'))

    def save_model(self, request, obj, form, change):
        obj.instance = request.session.get('admin_instance')
        obj.user = request.user
        obj.save()
        
    obj = None
    def get_form(self, request, obj=None, **kwargs):
        self.obj = obj 
        return super(ChallengeAdmin, self).get_form(request, obj, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'attachments' and getattr(self, 'obj', None):
            kwargs['queryset'] = Challenge.objects.get(id=self.obj.id).attachments.all()
        elif db_field.name == 'attachments':
            kwargs['queryset'] = Challenge.objects.filter(id=-2)

        if db_field.name == 'comments' and getattr(self, 'obj', None):
            kwargs['queryset'] = Challenge.objects.get(id=self.obj.id).comments.all()
        elif db_field.name == 'comments':
            kwargs['queryset'] = Challenge.objects.filter(id=-2)
        return super(ChallengeAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

#TODO: Split this out eventually into it's own project. Make sure that it goes after challenges
#Perhaps it should be called playerchallenges
#Once this is done make the foreign key point to Challenge
class PlayerChallenge(models.Model):
    accepted = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    response_type = models.CharField(max_length=30, blank=True, null=True)

    attachments = models.ManyToManyField(Attachment, blank=True, null=True)
    response = models.ForeignKey(CommentResponse, null=True, blank=True)
    challenge = models.ForeignKey(Challenge)
    player = models.ForeignKey(User)
    
    def __unicode__(self):
        label = self.player.username +"_"+ self.challenge.description
        return label[:25]
