__all__ = ( 
    'PlayerActivityType',
    'PlayerActivity', 
    'PlayerMapActivity', 
    'PlayerEmpathyActivity', 
    'MultiChoiceActivity', 
)

import datetime
from stream import utils as stream_utils
from stream.models import Action
from nani.models import TranslatableModel, TranslatedFields
from nani.manager import TranslationManager
from cache_utils.decorators import cached

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_delete, post_save

from django.contrib.auth.models import User
from django.contrib.contenttypes import generic

from web.attachments.models import Attachment
from web.comments.models import Comment
from web.missions.models import Mission, invalidate_mission
from web.reports.models import Activity
from web.instances.models import Instance
#from web.accounts.models import invalidate_prof_per_instance

import logging
log = logging.getLogger(__name__)

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

#class PlayerActivityManager(TranslationManager):
#    pass

class PlayerActivityBase(TranslatableModel):

    creationUser = models.ForeignKey(User, verbose_name="created by")
    mission = models.ForeignKey(Mission, related_name='%(app_label)s_%(class)s_related')
    type = models.ForeignKey(PlayerActivityType)
    createDate = models.DateTimeField(editable=False)
    points = models.IntegerField(blank=True, null=True, default=None)
    attachment = models.ManyToManyField(Attachment, blank=True, null=True)
    comments = generic.GenericRelation(Comment)
    comment_required = models.BooleanField('comment required', default=True)
    is_player_submittd = models.BooleanField("is player submitted?", default=False)

    #objects = PlayerActivityManager()

    #def get_children(self):
    #    rel_objs = self._meta.get_all_related_objects()
    #    return [getattr(self, x.get_accessor_name()) for x in rel_objs if x.model != type(self)]

    @property
    def activity_type_readable(self):
        @cached(60*60*168)
        def this_type(pk):
            return self.type.type
        return this_type(self.pk)

    def get_points(self):
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

    def trivia_answers(self):
        return filter(lambda c: c.trivia_correct_answer is True, self.answer_choices.all() if hasattr(self, 'answer_choices') else [])

    def get_trivia_answer(self):
        # This will work for multi_response activities only
        # which is what the requirements are for now
        # in the future may need to update to work for other
        # activity types
        trivia_answers = self.trivia_answers()
        if len(trivia_answers) > 0:
            return trivia_answers[0]

    def is_trivia(self):
        @cached(60*60*24*7)
        def is_trivia_by_pk(pk):
            return len(self.trivia_answers()) > 0
        return is_trivia_by_pk(self.pk)

    #@property
    #def completed_user_count(self):
    #    # the count of users completing an activity
    #    # comes from the activity stream
    #    d = {
    #        'empathy':'action_object_playerempathyactivity',
    #        'map':'action_object_playermapactivity',
    #    }
    #    action_object = d.get(self.type.type, 'action_object_playeractivity')
    #    kwargs={
    #        'verb':'activity_completed', 
    #        action_object:self,
    #    }
    #    return Action.objects.filter(**kwargs).count()

    @property
    def completed_count(self):
        actions = Action.objects.get_for_action_object(self)
        all_completed = filter(lambda a: a.verb == "activity_completed", actions)
        return len(all_completed)

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

    @property
    def stream_action_title(self):
        return self.__unicode__()

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
        if not self.createDate:
            self.createDate = datetime.datetime.now()
        super(PlayerActivity, self).save(*args, **kwargs)


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

    @property
    def stream_action_title(self):
        return self.__unicode__()

    def __unicode__(self):
        s = self.safe_translation_getter('name', None)
        if s is None:
            translated = self.__class__.objects.language(settings.LANGUAGE_CODE).get(pk=self.pk)
            s = translated.safe_translation_getter('name', str(self.pk))
        return s

    def save(self, *args, **kwargs):
        if not self.createDate:
            self.createDate = datetime.datetime.now()

        self.type = PlayerActivityType.objects.get(type="map")
        super(PlayerMapActivity, self).save(*args, **kwargs)


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

    @property
    def stream_action_title(self):
        return self.__unicode__()

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
        if not self.createDate:
            self.createDate = datetime.datetime.now()

        self.type = PlayerActivityType.objects.get(type="empathy")
        super(PlayerEmpathyActivity, self).save(*args, **kwargs)


class MultiChoiceActivity(TranslatableModel):
    """
    This seems to be misnamed. These are answers to activities with multiple
    choices.
    """
    activity = models.ForeignKey(PlayerActivity, related_name='answer_choices')

    # this field signifies that the multi-response question is of type
    # `Trivia`.
    #
    trivia_correct_answer = models.BooleanField(default=False, verbose_name="The correct answer to a trivia question")

    translations = TranslatedFields(
        value = models.CharField(max_length=255),
    )
    
    def is_completed(self, answerUser):
        return self.multi_choice_answers.filter(answerUser=answerUser).count() > 0

    class Meta:
        verbose_name = 'An Available Answer to a Single/Multiple Choice Activity'
        verbose_name_plural = 'Available Answers to Single/Multiple Choice Activities' 
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

#@receiver(pre_delete, sender=PlayerActivity, dispatch_uid='web.playeractivities.models')
#@receiver(pre_delete, sender=PlayerMapActivity, dispatch_uid='web.playeractivities.models')
#@receiver(pre_delete, sender=PlayerEmpathyActivity, dispatch_uid='web.playeractivities.models')
#def remove_url_from_news_feeds(sender, **kwargs):     
#    instance = kwargs['instance']
#    Activity.objects.filter(url=instance.get_activity_url()).update(url='')

# invalidate cache for 'missions' group
post_save.connect(invalidate_mission, PlayerActivity)
post_save.connect(invalidate_mission, PlayerMapActivity)
post_save.connect(invalidate_mission, PlayerEmpathyActivity)

#post_save.connect(invalidate_prof_per_instance, PlayerActivity)
#post_save.connect(invalidate_prof_per_instance, PlayerMapActivity)
#post_save.connect(invalidate_prof_per_instance, PlayerEmpathyActivity)

