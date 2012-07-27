#__all__ = ( 
#    'PlayerActivityType',
#    'PlayerActivity', 
#    'PlayerMapActivity', 
#    'PlayerEmpathyActivity', 
#    'MultiChoiceActivity', 
#)

import datetime
import os.path

from gmapsfield.fields import GoogleMapsField
from stream import utils as stream_utils
from stream.models import Action
from nani.models import TranslatableModel, TranslatedFields
from nani.manager import TranslationManager
from cache_utils.decorators import cached

from django.conf import settings
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save, post_delete
from django.db import models
from django.dispatch import receiver

from django.contrib.auth.models import User
from django.contrib.contenttypes import generic

from web.attachments_v2.models import Attachment
from web.comments.models import Comment
from web.missions.models import Mission, invalidate_mission #, invalidate_activities_for_mission
#from web.accounts.models import invalidate_prof_per_instance

import logging
log = logging.getLogger(__name__)

def determine_path(instance, filename):
    return 'uploads/'+ str(instance.creationUser.id) +'/'+ filename


class ChallengeType(models.Model):
    type = models.CharField(max_length=255)
    displayType = models.CharField(max_length=255)
    defaultPoints = models.IntegerField(default=10)

    class Meta:
        verbose_name_plural = 'Challenge Types'

    def __unicode__(self):
        return self.type

    class Meta:
        db_table = 'player_activities_playeractivitytype'

#class PlayerActivityManager(TranslationManager):
#    pass

class ChallengeBase(TranslatableModel):

    (SINGLE_RESPONSE, MULTI_RESPONSE, MAP, EMPATHY, OPEN_ENDED) = xrange(5)

    CHALLENGE_TYPES = (
        (SINGLE_RESPONSE, 'Single Response'),
        (MULTI_RESPONSE, 'Multiple Responses'),
        (MAP, 'Map'),
        (EMPATHY, 'Empathy'),
        (OPEN_ENDED, 'Open Ended'),
    )

    creationUser = models.ForeignKey(User, verbose_name="created by")
    mission = models.ForeignKey(Mission, related_name='%(app_label)s_%(class)s_related')

    # type field is marked for deletion
    # run the datamigration `merge_challenge_types` to convert to the
    # field `challenge_type`
    type = models.ForeignKey(ChallengeType)

    challenge_type = models.IntegerField(max_length=1, choices=CHALLENGE_TYPES, null=True)
    createDate = models.DateTimeField(editable=False)
    points = models.IntegerField(blank=True, null=True, default=None)
    attachment = models.ManyToManyField(Attachment, blank=True, null=True)
    comments = generic.GenericRelation(Comment)
    comment_required = models.BooleanField('comment required', default=True)
    is_player_submitted = models.BooleanField("is player submitted?", default=False)

    #objects = PlayerActivityManager()

    class Meta:
        abstract = True

    #def get_children(self):
    #    rel_objs = self._meta.get_all_related_objects()
    #    return [getattr(self, x.get_accessor_name()) for x in rel_objs if x.model != type(self)]

    def get_url_by_action(self, action):
        return reverse('missions:challenges:%s' % \
                slugify(self.get_challenge_type_display())
                +'-%s' % action,
                        args=(self.mission.pk, self.pk,))
    @property
    def overview_url(self):
        return self.get_url_by_action('overview')

    @property
    def play_url(self):
        return self.get_url_by_action('play')

    @property
    def activity_type_readable(self):
        @cached(60*60*168)
        def this_type(pk):
            return self.type.type
        return this_type(self.pk)

    @classmethod
    def get_display_type_by_const(self, const):
        """ lookup on challenge types """
        for type_pair in self.CHALLENGE_TYPES:
            if type_pair[0] == const:
                return slugify(type_pair[1])

    def get_points(self):
        @cached(60*60*168, 'activity_points')
        def this_activity_points(pk):
            return self.type.defaultPoints if self.points == None else self.points
        return this_activity_points(self.pk)

    def is_completed(self, answerUser):
        if self.type.type == 'multi_response':
            return MultiChoiceActivity.objects.\
                    filter(multichoice_answers__user=answerUser, activity=self).exists()
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
        #log.debug("%s completed %s" % (self.__unicode__(), len(all_completed)))
        return len(all_completed)

    def is_past(self):
        return self.mission.end_date < datetime.datetime.now()


class Challenge(ChallengeBase):

    translations = TranslatedFields(
        name = models.CharField(max_length=255),
        question = models.CharField(max_length=1000),
        instructions = models.CharField(max_length=255, null=True, blank=True),
        addInstructions = models.CharField(max_length=255, null=True, blank=True),
        meta = {'ordering': ['name'],
                'db_table': 'player_activities_playeractivity_translation',
               },
    )

    def __unicode__(self):
        return "challenge #%s" % self.pk
        #s = self.safe_translation_getter('name', None)
        #if s is None:
        #    translated = self.__class__.objects.language(settings.LANGUAGE_CODE).get(pk=self.pk)
        #    s = translated.safe_translation_getter('name', str(self.pk))
        #return s

    class Meta:
        verbose_name_plural = 'Challenges'
        db_table = 'player_activities_playeractivity'

    #@models.permalink --> breaks in localurl
    def get_absolute_url(self):
        return os.path.join(
                os.path.join(
                        'https://' if settings.DEBUG == False else 'http://',
                        self.mission.instance_city_domain(self.mission.instance.pk)
                ),
                self.get_overview_url()[1:]
        )
    @property
    def stream_action_title(self):
        return self.__unicode__()

    @property
    def stream_action_title(self):
        return self.__unicode__()

    def save(self, *args, **kwargs):
        if not self.createDate:
            self.createDate = datetime.datetime.now()
        super(Challenge, self).save(*args, **kwargs)


class MapChallenge(ChallengeBase):
    maxNumMarkers = models.IntegerField(default=5)

    translations = TranslatedFields(
        name = models.CharField(max_length=255),
        question = models.CharField(max_length=1000),
        instructions = models.CharField(max_length=255, null=True, blank=True),
        addInstructions = models.CharField(max_length=255, null=True, blank=True),
        meta = {'ordering': ['name'],
                'db_table': 'player_activities_playermapactivity_translation',
        },
    )

    def __unicode__(self):
        return "map challenge #%s" % self.pk
        #s = self.safe_translation_getter('name', None)
        #if s is None:
        #    translated = self.__class__.objects.language(settings.LANGUAGE_CODE).get(pk=self.pk)
        #    s = translated.safe_translation_getter('name', str(self.pk))
        #return s

    class Meta:
        verbose_name_plural = 'Player Map Challenges'
        db_table = 'player_activities_playermapactivity'

    @property
    def stream_action_title(self):
        return self.__unicode__()

    def save(self, *args, **kwargs):
        if not self.createDate:
            self.createDate = datetime.datetime.now()
        if self.challenge_type is None:
            self.challenge_type = Challenge.MAP
        super(MapChallenge, self).save(*args, **kwargs)


class EmpathyChallenge(ChallengeBase):
    avatar = models.ImageField(upload_to=determine_path, null=True, blank=True)
    translations = TranslatedFields(
        bio = models.TextField(max_length=1000),
        name = models.CharField(max_length=255),
        question = models.CharField(max_length=1000),
        instructions = models.CharField(max_length=255, null=True, blank=True),
        addInstructions = models.CharField(max_length=255, null=True, blank=True),
        meta = {'db_table': 'player_activities_playerempathyactivity_translation', },
    )

    def __unicode__(self):
        return "empathy challenge #%s" % self.pk
        #s = self.safe_translation_getter('name', None)
        #if s is None:
        #    translated = self.__class__.objects.language(settings.LANGUAGE_CODE).get(pk=self.pk)
        #    s = translated.safe_translation_getter('name', str(self.pk))
        #return s

    @models.permalink
    def get_absolute_url(self):
        return ('activities:empathy-overview', (self.pk,))

    class Meta:
        verbose_name_plural = 'Empathy Challenges'
        db_table = 'player_activities_playerempathyactivity'

    @property
    def stream_action_title(self):
        return self.__unicode__()

    def save(self, *args, **kwargs):
        if not self.createDate:
            self.createDate = datetime.datetime.now()
        if self.challenge_type is None:
            self.challenge_type = Challenge.EMPATHY
        super(EmpathyChallenge, self).save(*args, **kwargs)


class MultiChoiceActivityManager(TranslationManager):

    @cached(60*60*24*7)
    def by_activity(self, activity):
        log.debug("getting answers for %s. ** not cached **" % activity)
        return self.filter(activity=activity)


class MultiChoiceActivity(TranslatableModel):
    """
    This seems to be misnamed. These are answers to activities with multiple
    choices.
    """
    activity = models.ForeignKey(Challenge, related_name='answer_choices')

    # this field signifies that the multi-response question is of type
    # `Trivia`.
    #
    trivia_correct_answer = models.BooleanField(default=False, verbose_name="The correct answer to a trivia question")

    translations = TranslatedFields(
        value = models.CharField(max_length=255),
        meta = {'db_table': 'player_activities_multichoiceactivity_translation', },
    )

    objects = MultiChoiceActivityManager()

    def is_completed(self, answerUser):
        return self.multi_choice_answers.filter(answerUser=answerUser).count() > 0

    class Meta:
        verbose_name = 'An Available Answer to a Single/Multiple Choice Challenge'
        verbose_name_plural = 'Available Answers to Single/Multiple Choice Challenges' 
        db_table = 'player_activities_multichoiceactivity'

    def __unicode__(self):
        return "multichoice option #%s" % self.pk
        #s = self.safe_translation_getter('value', None)
        #if s is None:
        #    translated = self.__class__.objects.language(settings.LANGUAGE_CODE).get(pk=self.pk)
        #    s = translated.safe_translation_getter('value', str(self.pk))
        #return s

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


class Answer(models.Model):
    answerUser = models.ForeignKey(User, editable=False, related_name='answers')
    comments = generic.GenericRelation(Comment)
    createDate = models.DateTimeField(editable=False)

    class Meta:
        ordering = ('-createDate',)
        db_table = 'answers_answer'

    def save(self, *args, **kwargs):
        self.createDate = datetime.datetime.now()
        super(Answer, self).save(*args, **kwargs)

    #@models.permalink --> breaks in localeurl
    def get_absolute_url(self):
        #return ("player_activities:overview", [self.activity.id])
        return self.activity.get_absolute_url()

class AnswerSingleResponseManager(models.Manager):

    def my_answers_by_activity(self, activity, user):
        return self.answers_by_activity(activity).filter(answerUser=user)

    def my_answers_by_activity_as_str(self, activity, user):
        my_answers = self.my_answers_by_activity(activity, user)
        return ";".join([a.selected.value for a in my_answers])

    def my_answers_by_activity_likes_count(self, activity, user):
        my_answers = self.my_answers_by_activity(activity, user)
        # in theory there should be one answer for each challenge
        if my_answers.count() > 0:
            my_comments = my_answers[0].comments.all()
            if my_comments.count() > 0:
                return my_comments[0].likes.all().count()
        return 0

    #@cached(60*60*24*7)
    def answers_by_activity(self, activity):
        return self.filter(activity=activity)

class AnswerSingleResponse(Answer):
    selected = models.ForeignKey(MultiChoiceActivity, related_name='singleresponse_answers')
    activity = models.ForeignKey(Challenge, related_name='singleresponse_answers')

    objects = AnswerSingleResponseManager()

    def __unicode__(self):
        return _(u'an answer to %s' % self.activity)

    class Meta:
        db_table = 'answers_answersingleresponse'


class AnswerMultiChoiceManager(models.Manager):

    def my_answers_by_activity(self, activity, user):
        return self.answers_by_activity(activity).filter(user=user)

    def my_answers_by_activity_as_str(self, activity, user):
        my_answers = self.my_answers_by_activity(activity, user)
        return ";".join([a.option_value for a in my_answers])

    def my_answers_by_activity_likes_count(self, activity, user):
        my_answers = self.my_answers_by_activity(activity, user)
        # in theory there should be one answer for each challenge
        if my_answers.count() > 0:
            my_comments = my_answers[0].comments.all()
            if my_comments.count() > 0:
                return my_comments[0].likes.all().count()
        return 0

    #@cached(60*60*24*7)
    def answers_by_activity(self, activity):
        return self.filter(option__activity=activity)

#This is nasty but it's the simple way to get many checked values
#for the user stored
class AnswerMultiChoice(models.Model):
    user = models.ForeignKey(User)
    option = models.ForeignKey(MultiChoiceActivity, related_name='multichoice_answers')
    comments = generic.GenericRelation(Comment)

    objects = AnswerMultiChoiceManager()

    def __unicode__(self):
        return self.option.value

    class Meta:
        db_table = 'answers_answermultichoice'

    #@models.permalink --> breaks in localurl
    def get_absolute_url(self):
        #return ("player_activities:overview", [self.option.activity.id])
        return self.option.activity.get_absolute_url()

    @property
    def option_value(self):
        @cached(60*60*24*7)
        def this_option_value(answer_id):
            return self.option.value
        return this_option_value(self.pk)

    def get_user(self):
        @cached(60*60*24*7)
        def this_user(answer_id):
            return self.user
        return this_user(self.pk)


class AnswerMapManager(models.Manager):

    def my_answers_by_activity(self, activity, user):
        return self.answers_by_activity(activity).filter(answerUser=user)

    def my_answers_by_activity_as_str(self, activity, user):
        my_answers = self.my_answers_by_activity(activity, user)
        # in theory there should be one answer for each challenge
        if my_answers.count() > 0:
            return ", ".join(map(lambda c: str(c), my_answers[0].map.coordinates))
        return ''

    def my_answers_by_activity_likes_count(self, activity, user):
        my_answers = self.my_answers_by_activity(activity, user)
        # in theory there should be one answer for each challenge
        if my_answers.count() > 0:
            my_comments = my_answers[0].comments.all()
            if my_comments.count() > 0:
                return my_comments[0].likes.all().count()
        return 0

    #@cached(60*60*24*7)
    def answers_by_activity(self, activity):
        return self.filter(activity=activity)


class AnswerMap(Answer):
    map = GoogleMapsField()
    activity = models.ForeignKey(MapChallenge, related_name='map_answers')

    objects = AnswerMapManager()

    def __unicode__(self):
        return _(u'an answer to %s' % self.activity)

    class Meta:
        db_table = 'answers_answermap'

    #@models.permalink --> breaks in localurl
    def get_absolute_url(self):
        #return ("player_activities:map-overview", [self.activity.id])
        return self.activity.get_absolute_url()

class AnswerEmpathyManager(models.Manager):

    def my_answers_by_activity(self, activity, user):
        return self.answers_by_activity(activity).filter(answerUser=user)

    def my_answers_by_activity_as_str(self, activity, user):
        my_answers = self.my_answers_by_activity(activity, user)
        # in theory there should be one answer for each challenge
        if my_answers.count() > 0:
            return ", ".join(my_answers[0].comments.values_list('message', flat=True))
        return ""

    def my_answers_by_activity_likes_count(self, activity, user):
        my_answers = self.my_answers_by_activity(activity, user)
        # in theory there should be one answer for each challenge
        if my_answers.count() > 0:
            my_comments = my_answers[0].comments.all()
            if my_comments.count() > 0:
                return my_comments[0].likes.all().count()
        return 0

    #@cached(60*60*24*7)
    def answers_by_activity(self, activity):
        return self.filter(activity=activity)

class AnswerEmpathy(Answer):
    activity = models.ForeignKey(EmpathyChallenge, related_name='empathy_answers')

    objects = AnswerEmpathyManager()

    def __unicode__(self):
        return _(u'an answer to %s' % self.activity)

    class Meta:
        db_table = 'answers_answerempathy'

    #@models.permalink --> breaks in localurl
    def get_absolute_url(self):
        #return ("player_activities:empathy-overview", [self.activity.id])
        return self.activity.get_absolute_url()


class AnswerOpenEndedManager(models.Manager):

    def my_answers_by_activity(self, activity, user):
        return self.answers_by_activity(activity).filter(answerUser=user)

    def my_answers_by_activity_as_str(self, activity, user):
        my_answers = self.my_answers_by_activity(activity, user)
        if my_answers.count() > 0:
            return ", ".join(my_answers[0].comments.values_list('message', flat=True))
        return ""

    def my_answers_by_activity_likes_count(self, activity, user):
        my_answers = self.my_answers_by_activity(activity, user)
        # in theory there should be one answer for each challenge
        if my_answers.count() > 0:
            my_comments = my_answers[0].comments.all()
            if my_comments.count() > 0:
                return my_comments[0].likes.all().count()
        return 0

    #@cached(60*60*24*7)
    def answers_by_activity(self, activity):
        return self.filter(activity=activity)


class AnswerOpenEnded(Answer):
    activity = models.ForeignKey(Challenge, related_name='openended_answers')

    objects = AnswerOpenEndedManager()

    def __unicode__(self):
        return _(u'an answer to %s' % self.activity)

    class Meta:
        db_table = 'answers_answeropenended'


#django-stream registrations
stream_utils.register_action_object(Challenge)
stream_utils.register_target(Challenge)

stream_utils.register_action_object(Challenge)
stream_utils.register_target(Challenge)

stream_utils.register_action_object(MapChallenge)
stream_utils.register_target(MapChallenge)

stream_utils.register_action_object(EmpathyChallenge)
stream_utils.register_target(EmpathyChallenge)

#@receiver(pre_delete, sender=Challenge, dispatch_uid='web.playeractivities.models')
#@receiver(pre_delete, sender=PlayerMapActivity, dispatch_uid='web.playeractivities.models')
#@receiver(pre_delete, sender=PlayerEmpathyActivity, dispatch_uid='web.playeractivities.models')
#def remove_url_from_news_feeds(sender, **kwargs):     
#    instance = kwargs['instance']
#    Activity.objects.filter(url=instance.get_activity_url()).update(url='')

# invalidate cache for 'missions' group
post_save.connect(invalidate_mission, Challenge)
post_save.connect(invalidate_mission, MapChallenge)
post_save.connect(invalidate_mission, EmpathyChallenge)

#post_save.connect(invalidate_prof_per_instance, Challenge)
#post_save.connect(invalidate_prof_per_instance, PlayerMapActivity)
#post_save.connect(invalidate_prof_per_instance, PlayerEmpathyActivity)

#post_delete.connect(invalidate_activities_for_mission, Challenge)
#post_delete.connect(invalidate_activities_for_mission, PlayerMapActivity)
#post_delete.connect(invalidate_activities_for_mission, PlayerEmpathyActivity)
