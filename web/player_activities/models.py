import datetime
from stream import utils as stream_utils
from nani.models import TranslatableModel, TranslatedFields

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_delete, post_save

from django.contrib.auth.models import User
from django.contrib.contenttypes import generic

from attachments.models import Attachment
from comments.models import Comment
from missions.models import Mission
from reports.models import Activity
from instances.models import Instance

__all__ = ( 
    'PlayerActivityType',
    'PlayerActivity', 
    'PlayerMapActivity', 
    'PlayerEmpathyActivity', 
    'MultiChoiceActivity', 
    'PlayerActivityOfficialResponse',
    'MapOfficialResponse',
    'EmpathyOfficialResponse',
)

def determine_path(instance, filename):
    return 'uploads/'+ str(instance.creationUser.id) +'/'+ filename

class PlayerActivityType(models.Model):
    type = models.CharField(max_length=255)
    displayType = models.CharField(max_length=255)
    defaultPoints = models.IntegerField(default=10)

    class Meta:
        verbose_name_plural = 'Player Activity Types'

    def __unicode__(self):
        return self.type

class PlayerActivityBase(TranslatableModel):

    creationUser = models.ForeignKey(User, verbose_name="created by")
    mission = models.ForeignKey(Mission, related_name='%(app_label)s_%(class)s_related')
    type = models.ForeignKey(PlayerActivityType)
    createDate = models.DateTimeField(editable=False)
    points = models.IntegerField(blank=True, null=True, default=None)
    attachment = models.ManyToManyField(Attachment, blank=True, null=True)
    comments = generic.GenericRelation(Comment)    

    def getPoints(self):
        if self.points == None:
            return self.type.defaultPoints
        else:
            return self.points
        
    def is_completed(self, answerUser):
        if self.type.type == 'multi_response':
            answers = MultiChoiceActivity.objects.filter(multichoice_answers__user=answerUser, activity=self).count()
            return answers > 0
        else:
            for answer_klass_name in ['AnswerEmpathy', 'AnswerMap', 'AnswerSingleResponse', 'AnswerOpenEnded']:
                related_name = answer_klass_name.replace('Answer', '').lower() + '_answers'
                if hasattr(self, related_name):
                    if getattr(self, related_name).filter(answerUser=answerUser).count():
                        return True
        return False

    def is_past(self):
        return self.mission.end_date < datetime.datetime.now()

    class Meta:
        abstract = True

class PlayerActivity(PlayerActivityBase):

    translations = TranslatedFields(
        name = models.CharField(max_length=255),
        question = models.CharField(max_length=1000),
        instructions = models.CharField(max_length=255, null=True, blank=True),
        addInstructions = models.CharField(max_length=255, null=True, blank=True),
        meta = {'ordering': ['name']},
    )

    class Meta:
        verbose_name_plural = 'Player Activities'

    @models.permalink
    def get_absolute_url(self):
        return ('activities:overview', (self.pk,))

    def get_overview_url(self):
        return reverse('activities:overview', args=(self.pk,))

    def get_activity_url(self):
        return reverse('activities:activity', args=(self.pk,))

    def get_replay_url(self):
        return reverse('activities:replay', args=(self.pk,))

    def __unicode__(self):
        s = self.safe_translation_getter('name', None)
        if s is None:
            translated = self.__class__.objects.language(settings.LANGUAGE_CODE).get(pk=self.pk)
            s = translated.safe_translation_getter('name', str(self.pk))
        return s

    @property
    def stream_action_title(self):
        return self.__unicode__()

    def save(self, *args, **kwargs):
        self.createDate = datetime.datetime.now()
        super(PlayerActivity, self).save(*args, **kwargs)



class PlayerActivityOfficialResponse(models.Model):
    activity = models.OneToOneField(PlayerActivity, unique=True)
    response = models.TextField(max_length=500, blank=True, default='')
    comments = generic.GenericRelation(Comment)
    date_added = models.DateTimeField(editable=False, auto_now_add=True)

    @models.permalink
    def get_absolute_url(self):
        return ('activities:overview', (self.activity.pk,))

    def __unicode__(self):
        return u"Official Response (%s) for <%s> " % (self.response[:10], self.activity.mission.title )

    @property
    def stream_action_title(self):
        return self.response

    @property
    def instance(self):
        return self.activity.mission.instance

    @property
    def mission(self):
        return self.activity.mission

class PlayerMapActivity(PlayerActivityBase):
    maxNumMarkers = models.IntegerField(default=5)
    #django-nani complains that no translated fields exist on a sublclass of TraslatableModel

    translations = TranslatedFields(
        name = models.CharField(max_length=255),
        question = models.CharField(max_length=1000),
        instructions = models.CharField(max_length=255, null=True, blank=True),
        addInstructions = models.CharField(max_length=255, null=True, blank=True),
        meta = {'ordering': ['name']},
    )
    
    class Meta:
        verbose_name_plural = 'Player Map Activities'

    @models.permalink
    def get_absolute_url(self):
        return ('activities:map-overview', (self.pk,))

    def get_overview_url(self):
        return reverse('activities:map-overview', args=(self.pk,))

    def get_activity_url(self):
        return reverse('activities:map-activity', args=(self.pk,))

    def get_replay_url(self):
        return reverse('activities:map-replay', args=(self.pk,))

    def __unicode__(self):
        s = self.safe_translation_getter('name', None)
        if s is None:
            translated = self.__class__.objects.language(settings.LANGUAGE_CODE).get(pk=self.pk)
            s = translated.safe_translation_getter('name', str(self.pk))
        return s

    def save(self, *args, **kwargs):
        self.createDate = datetime.datetime.now()
        self.type = PlayerActivityType.objects.get(type="map")
        super(PlayerMapActivity, self).save(*args, **kwargs)


class MapOfficialResponse(models.Model):
    activity = models.OneToOneField(PlayerMapActivity, unique=True)
    response = models.TextField(max_length=500, blank=True, default='')
    comments = generic.GenericRelation(Comment)
    date_added = models.DateTimeField(editable=False, auto_now_add=True)

    @models.permalink
    def get_absolute_url(self):
        return ('activities:map-overview', (self.activity.pk,))

    def __unicode__(self):
        return "Official Response (%s) for <%s> " % (self.response[:10], self.activity.mission.title )

    @property
    def stream_action_title(self):
        return self.response

    @property
    def instance(self):
        return self.activity.mission.instance

    @property
    def mission(self):
        return self.activity.mission


class PlayerEmpathyActivity(PlayerActivityBase):
    avatar = models.ImageField(upload_to=determine_path, null=True, blank=True)
    translations = TranslatedFields(        
        bio = models.TextField(max_length=1000),
        name = models.CharField(max_length=255),
        question = models.CharField(max_length=1000),
        instructions = models.CharField(max_length=255, null=True, blank=True),
        addInstructions = models.CharField(max_length=255, null=True, blank=True),
    )
    
    class Meta:
        verbose_name_plural = 'Player Empathy Activities'

    @models.permalink
    def get_absolute_url(self):
        return ('activities:empathy-overview', (self.pk,))

    def __unicode__(self):
        s = self.safe_translation_getter('name', None)
        if s is None:
            translated = self.__class__.objects.language(settings.LANGUAGE_CODE).get(pk=self.pk)
            s = translated.safe_translation_getter('name', str(self.pk))
        return s

    @property
    def stream_action_title(self):
        return self.__unicode__()

    def get_overview_url(self):
        return reverse('activities:empathy-overview', args=(self.pk,))

    def get_activity_url(self):
        return reverse('activities:empathy-activity', args=(self.pk,))

    def get_replay_url(self):
        return reverse('activities:empathy-replay', args=(self.pk,))

    def save(self, *args, **kwargs):
        self.createDate = datetime.datetime.now()
        self.type = PlayerActivityType.objects.get(type="empathy")
        super(PlayerEmpathyActivity, self).save(*args, **kwargs)


class EmpathyOfficialResponse(models.Model):
    activity = models.OneToOneField(PlayerEmpathyActivity, unique=True)
    response = models.TextField(max_length=500, blank=True, default='')
    comments = generic.GenericRelation(Comment)
    date_added = models.DateTimeField(editable=False, auto_now_add=True)

    @models.permalink
    def get_absolute_url(self):
        return ('activities:empathy-overview', (self.activity.pk,))

    def __unicode__(self):
        return u"Official Response (%s) for <%s> " % (self.response[:10], self.activity.mission.title )

    @property
    def stream_action_title(self):
        return self.response

    @property
    def instance(self):
        return self.activity.mission.instance

    @property
    def mission(self):
        return self.activity.mission


class MultiChoiceActivity(TranslatableModel):
    """
    This seems to be misnamed. These are answers to activities with multiple
    choices.
    """
    activity = models.ForeignKey(PlayerActivity, related_name='answer_choices')

    translations = TranslatedFields(
        value = models.CharField(max_length=255),
    )
    
    def is_completed(self, answerUser):
        return self.multi_choice_answers.filter(answerUser=answerUser).count() > 0

    class Meta:
        verbose_name = 'Multiple Choice Activity'
        verbose_name_plural = 'Multiple Choice Activities'

    def __unicode__(self):
        s = self.safe_translation_getter('value', None)
        if s is None:
            translated = self.__class__.objects.language(settings.LANGUAGE_CODE).get(pk=self.pk)
            s = translated.safe_translation_getter('value', str(self.pk))
        return s

    @property
    def activity_type(self):
        return self.activity.type

    @property
    def activity_points(self):
        return self.activity.points

    @property
    def mission(self):
        return self.activity.mission

    @property
    def mission_title(self):
        return self.activity.mission.title


#django-stream registrations
stream_utils.register_action_object(PlayerActivity)
stream_utils.register_target(PlayerActivity)

stream_utils.register_action_object(PlayerActivity)
stream_utils.register_target(PlayerActivity)

stream_utils.register_action_object(PlayerMapActivity)
stream_utils.register_target(PlayerMapActivity)

stream_utils.register_action_object(PlayerEmpathyActivity)
stream_utils.register_target(PlayerEmpathyActivity)

stream_utils.register_action_object(PlayerActivityOfficialResponse)
stream_utils.register_action_object(MapOfficialResponse)
stream_utils.register_action_object(EmpathyOfficialResponse)

@receiver(pre_delete, sender=PlayerActivity, dispatch_uid='web.playeractivities.models')
@receiver(pre_delete, sender=PlayerMapActivity, dispatch_uid='web.playeractivities.models')
@receiver(pre_delete, sender=PlayerEmpathyActivity, dispatch_uid='web.playeractivities.models')
def remove_url_from_news_feeds(sender, **kwargs):     
    instance = kwargs['instance']
    Activity.objects.filter(url=instance.get_activity_url()).update(url='')

@receiver(post_save, sender=PlayerActivityOfficialResponse, dispatch_uid='web.playeractivities.models')
@receiver(post_save, sender=MapOfficialResponse, dispatch_uid='web.playeractivities.models')
@receiver(post_save, sender=EmpathyOfficialResponse, dispatch_uid='web.playeractivities.models')
def add_response_as_comment(sender, **kwargs):
    created =  kwargs.get('created')
    obj = kwargs.get('instance')
    active_instance = Instance.objects.language(settings.LANGUAGE_CODE)[0]

    user = User.objects.filter(is_superuser=True)[0]
    if created:
        comment = Comment.objects.create(
                user = user,
                message = obj.response,
                object_id = obj.pk,
                instance=active_instance,
        )
        obj.comments.add(comment)

        stream_utils.action.send(actor=user, verb='activity_official_response_created', target=obj.activity, action_object=obj, description='Official response created')

    else:
        Comment.objects.filter(object_id=obj.pk).update(message=obj.response)

