import datetime
import os.path

from gmapsfield.fields import GoogleMapsField
from stream import utils as stream_utils
from stream.models import Action
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

#from web.attachments_v2.models import Attachment
#from web.comments.models import Comment
from web.missions.models import Mission
from web.instances.models import BaseTreeNode

import logging
log = logging.getLogger(__name__)


class Challenge(BaseTreeNode):

    (SINGLE_RESPONSE, MULTI_RESPONSE, MAP, EMPATHY, OPEN_ENDED, BARRIER, FINAL_BARRIER) = xrange(7)

    CHALLENGE_TYPES = (
        (SINGLE_RESPONSE, 'Single Response'),
        (MULTI_RESPONSE, 'Multiple Responses'),
        (MAP, 'Map'),
        (EMPATHY, 'Empathy'),
        (OPEN_ENDED, 'Open Ended'),
        (BARRIER, 'Barrier'),
        (FINAL_BARRIER, 'Final Barrier'),
    )
    question = models.CharField(max_length=1000, default='')
    challenge_type = models.IntegerField(max_length=1, choices=CHALLENGE_TYPES, null=True)
    mission = models.ForeignKey(Mission, related_name='%(app_label)s_%(class)s_related')
    is_player_submitted = models.BooleanField("is player submitted?", default=False)

    created_by = models.ForeignKey(User, verbose_name="created by")
    created_date = models.DateTimeField(auto_now_add=True)

    #objects = ChallengeManager()
    def __unicode__(self):
        return self.question

    @property
    def overview_url(self):
        return self.get_url_by_action('overview')

    @property
    def play_url(self):
        return self.get_url_by_action('play')

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

    @property
    def completed_count(self):
        actions = Action.objects.get_for_action_object(self)
        all_completed = filter(lambda a: a.verb == "activity_completed", actions)
        #log.debug("%s completed %s" % (self.__unicode__(), len(all_completed)))
        return len(all_completed)

    def is_past(self):
        return self.mission.end_date < datetime.datetime.now()

class SingleResponseChallenge(Challenge):

    def save(self, *args, **kwargs):
        if self.challenge_type is None:
            self.challenge_type = Challenge.SINGLE_RESPONSE
        super(SingleResponseChallenge, self).save(*args, **kwargs)


class MultiResponseChallenge(Challenge):

    def save(self, *args, **kwargs):
        if self.challenge_type is None:
            self.challenge_type = Challenge.MULTI_RESPONSE
        super(MultiResponseChallenge, self).save(*args, **kwargs)


class BarrierChallenge(Challenge):

    def save(self, *args, **kwargs):
        if self.challenge_type is None:
            self.challenge_type = Challenge.MULTI_RESPONSE
        super(BarrierChallenge, self).save(*args, **kwargs)

class MapChallenge(Challenge):

    maxNumMarkers = models.IntegerField(default=5)

    class Meta:
        pass

    @property
    def stream_action_title(self):
        return self.__unicode__()

    def save(self, *args, **kwargs):
        if self.challenge_type is None:
            self.challenge_type = Challenge.MAP
        super(MapChallenge, self).save(*args, **kwargs)


class EmpathyChallenge(Challenge):

    def determine_path(instance, filename):
        return 'uploads/'+ str(instance.creationUser.id) +'/'+ filename

    bio_text = models.TextField(verbose_name="Bio", max_length=1000, default='')
    avatar = models.ImageField(upload_to=determine_path, null=True, blank=True)

    @models.permalink
    def get_absolute_url(self):
        return ''

    class Meta:
        pass

    @property
    def stream_action_title(self):
        return self.__unicode__()

    def save(self, *args, **kwargs):
        if self.challenge_type is None:
            self.challenge_type = Challenge.EMPATHY
        super(EmpathyChallenge, self).save(*args, **kwargs)


class AnswerChoiceManager(models.Manager):

    @cached(60*60*24*7)
    def by_challenge(self, challenge):
        return self.filter(challenge=challenge)


class AnswerChoice(models.Model):
    """ These are answer choices to single/multi response challenges """

    challenge = models.ForeignKey(Challenge, related_name='answer_choices')
    value = models.CharField(max_length=255)

    # this field signifies that the multi-response question is of type
    # `Trivia`.
    #
    trivia_correct_answer = models.BooleanField(default=False, verbose_name="The correct answer to a trivia question")

    objects = AnswerChoiceManager()

    def __unicode__(self):
        return self.value

class Answer(models.Model):
    """ user submitted response to a challenge """

    user = models.ForeignKey(User, editable=False, related_name='answers')
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        pass

    @models.permalink
    def get_absolute_url(self):
        return ""


class AnswerWithChoices(Answer):
    """ user submitted response to a single response challenge """

    selected = models.ManyToManyField(AnswerChoice, related_name='singleresponse_answers')
    activity = models.ForeignKey(Challenge, related_name='singleresponse_answers')

    #objects = AnswerSingleResponseManager()

    def __unicode__(self):
        return _(u'an answer to %s' % self.activity)


class AnswerMap(Answer):
    map = GoogleMapsField()
    challenge = models.ForeignKey(MapChallenge, related_name='map_answers')

    #objects = AnswerMapManager()

    def __unicode__(self):
        return _(u'an answer to %s' % self.activity)

    @models.permalink
    def get_absolute_url(self):
        return ''


class AnswerEmpathy(Answer):
    value = models.TextField(verbose_name="Answer Empathy", max_length=1000, default='')
    challenge = models.ForeignKey(EmpathyChallenge, related_name='empathy_answers')

    #objects = AnswerEmpathyManager()

    def __unicode__(self):
        return _(u'an answer to %s' % self.activity)

    @models.permalink
    def get_absolute_url(self):
        return ""


class AnswerOpenEnded(Answer):
    value = models.TextField(verbose_name="Answer Open Ended", max_length=1000, default='')
    challenge = models.ForeignKey(Challenge, related_name='openended_answers')

    #objects = AnswerOpenEndedManager()

    def __unicode__(self):
        return _(u'an answer to %s' % self.activity)


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
#post_save.connect(invalidate_mission, Challenge)
#post_save.connect(invalidate_mission, MapChallenge)
#post_save.connect(invalidate_mission, EmpathyChallenge)

#post_save.connect(invalidate_prof_per_instance, Challenge)
#post_save.connect(invalidate_prof_per_instance, PlayerMapActivity)
#post_save.connect(invalidate_prof_per_instance, PlayerEmpathyActivity)

#post_delete.connect(invalidate_activities_for_mission, Challenge)
#post_delete.connect(invalidate_activities_for_mission, PlayerMapActivity)
#post_delete.connect(invalidate_activities_for_mission, PlayerEmpathyActivity)
