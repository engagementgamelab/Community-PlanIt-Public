import datetime

from django.db import models

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic

from gmapsfield.fields import GoogleMapsField

from web.attachments.models import Attachment
from web.comments.models import Comment
from web.instances.models import Instance
from web.responses.comment.models import CommentResponse

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^gmapsfield\.fields\.GoogleMapsField"])

class ChallengeQueryMixin(object):
    def active(self):
        now = datetime.datetime.now()
        return self.filter(start_date__lte=now).filter(end_date__gte=now).order_by('start_date')

    def available(self, user):
        return self.active().exclude(player_challenges__player=user).order_by('start_date')

    def past(self):
        now = datetime.datetime.now()
        return self.filter(end_date__lt=now).order_by('start_date')

class ChallengeQuerySet(models.query.QuerySet, ChallengeQueryMixin):
    pass

class ChallengeManager(models.Manager, ChallengeQueryMixin):
    def get_query_set(self):
        return ChallengeQuerySet(self.model, using=self._db)

class Challenge(models.Model):
    map = GoogleMapsField()
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    flagged = models.BooleanField(default=0, editable=False)

    instance = models.ForeignKey(Instance, related_name='challenges')
    user = models.ForeignKey(User, editable=False)
    attachments = models.ManyToManyField(Attachment, blank=True)
    comments = generic.GenericRelation(Comment)
    game_type = models.CharField(max_length=45, editable=False)

    objects = ChallengeManager()

    class Meta:
        ordering = ['start_date']
    
    @models.permalink
    def get_absolute_url(self):
        return ('challenges_challenge', [str(self.id)])
    
    def is_active(self):
        now = datetime.datetime.now()
        return self.start_date <= now and now <= self.end_date
        
    def is_expired(self):
        return datetime.datetime.now() > self.end_date
    
    def is_started(self):
        return datetime.datetime.now() >= self.start_date
    
    def save(self):
        self.game_type = "challenge"
        #TODO: Make sure this is correct, the None map I am not sure about - BMH
        if self.map == "None":
            self.map = self.instance.location
        super(Challenge, self).save()

    def __unicode__(self):
        label = self.name or 'None'
        return label

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

class PlayerChallengeQueryMixin(object):
    def accepted(self):
        return self.filter(accepted=True, completed=False)

    def available(self):
        now = datetime.datetime.now()
        result = self.filter(accepted=False, completed=False)
        result = result.filter(challenge__start_date__lte=now, challenge__end_date__gte=now)
        return result

    def completed(self):
        return self.filter(completed=True)

    def declined(self):
        return self.filter(declined=True)

    def current(self):
        return self.filter(accepted=True, completed=False)

class PlayerChallengeQuerySet(models.query.QuerySet, PlayerChallengeQueryMixin):
    pass

class PlayerChallengeManager(models.Manager, PlayerChallengeQueryMixin):
    def get_query_set(self):
        return PlayerChallengeQuerySet(self.model, using=self._db)

class PlayerChallenge(models.Model):
    accepted = models.BooleanField(default=False)
    declined = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    response_type = models.CharField(max_length=30, blank=True, null=True)

    attachments = models.ManyToManyField(Attachment, blank=True, null=True)
    response = models.OneToOneField(CommentResponse, null=True, blank=True, related_name='player_challenge')
    challenge = models.ForeignKey(Challenge, related_name='player_challenges')
    player = models.ForeignKey(User, related_name='player_challenges')

    objects = PlayerChallengeManager()
    
    def __unicode__(self):
        label = self.player.username +"_"+ self.challenge.description
        return label[:25]
