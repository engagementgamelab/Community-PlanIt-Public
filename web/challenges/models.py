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

class Challenge(models.Model):
    map = GoogleMapsField()
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    flagged = models.IntegerField(default=0, editable=False)

    #TODO: Figure out why this is not required, or make it required. The view to add a challenge
    #expects an instance from the user profile so why can it be blank here?
    instance = models.ForeignKey(Instance, null=True, blank=True,editable=False)
    user = models.ForeignKey(User, editable=False)
    attachments = models.ManyToManyField(Attachment, blank=True)
    comments = models.ManyToManyField(Comment, blank=True)
    
    #TODO: Turn this into a view, GAH! -BMH
    def is_active(self):
        return self.end_date >= datetime.datetime.now()

    def is_expired(self):
        return self.end_date <= datetime.datetime.now()

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

class PlayerChallenge(models.Model):
    accepted = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    response_type = models.CharField(max_length=30, blank=True, null=True)

    attachments = models.ManyToManyField(Attachment, blank=True, null=True)
    response = models.ForeignKey(CommentResponse, null=True, blank=True)
    player = models.ForeignKey(User)
    challenge = models.ForeignKey(Challenge)

    def __unicode__(self):
        label = self.player.username +"_"+ self.challenge.description
        return label[:25]
