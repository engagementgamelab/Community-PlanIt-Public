import random
import datetime
import os.path

from gmapsfield.fields import GoogleMapsField
from cache_utils.decorators import cached
from polymorphic import PolymorphicModel

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.exceptions import ImproperlyConfigured
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save, post_delete
from django.db import models
from django.dispatch import receiver

from django.contrib.auth.models import User

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

    def challenge_upload(instance, filename):
        return 'attachments/{pk}/{filename}'.format(pk=instance.pk, filename=filename)

    # used by django-polymorphic-tree for self explanatory purpose
    can_have_children = True

    question = models.CharField(max_length=1000, default='')
    challenge_type = models.IntegerField(max_length=1, choices=CHALLENGE_TYPES, null=True)
    thumbnail = models.FileField(help_text="Thumb 164x100", upload_to=challenge_upload, blank=True, null=True)
    is_player_submitted = models.BooleanField("is player submitted?", default=False)

    created_by = models.ForeignKey(User, verbose_name="created by")
    created_date = models.DateTimeField(auto_now_add=True)

    #objects = ChallengeManager()

    def __unicode__(self):
        #if self.challenge_type is not None:
        #    return "%s [%s]" % (self.title, self.challenge_type_shortcut)
        return self.title

    @property
    def mission(self):
        return self.mission_cached(self.pk)

    @cached(60*60*24*365)
    def mission_cached(self, challenge_id):
        return self.parent

    @property
    def game(self):
        return self.game_cached(self.pk)

    @cached(60*60*24*365)
    def game_cached(self, challenge_id):
        return self.parent.parent

    @property
    def challenge_type_shortcut(self):
        return self.challenge_type_shortcut_cached(self.challenge_type)

    @cached(60*60*24*365)
    def challenge_type_shortcut_cached(self, challenge_type):
        return slugify(self.get_challenge_type_display())

    @property
    def play_url(self):
        return self.play_url_cached(self.pk)

    @cached(60*60*24*365)
    def play_url_cached(self, challenge_id):
        return reverse(
                'instances:missions:challenges:'+self.challenge_type_shortcut+'-play',
                args=(self.game.slug, self.mission.pk, challenge_id)
        )

    @property
    def overview_url(self):
        return self.overview_url_cached(self.pk)

    @cached(60*60*24*365)
    def overview_url_cached(self, challenge_id):
        return reverse(
                'instances:missions:challenges:'+self.challenge_type_shortcut+'-overview',
                args=(self.game.slug, self.mission.pk, challenge_id)
        )


class SingleResponseChallenge(Challenge):

    def save(self, *args, **kwargs):
        if self.challenge_type is None:
            self.challenge_type = Challenge.SINGLE_RESPONSE
        super(SingleResponseChallenge, self).save(*args, **kwargs)


class MultiResponseChallenge(Challenge):

    require_comment = models.BooleanField(default=False, verbose_name="Require players to submit a comment")

    def save(self, *args, **kwargs):
        if self.challenge_type is None:
            self.challenge_type = Challenge.MULTI_RESPONSE
        super(MultiResponseChallenge, self).save(*args, **kwargs)


class BarrierChallenge(Challenge):

    minimum_coins_to_play = models.IntegerField(default=0)

    @property
    def fifty_fifty_url(self):
        return reverse(
                'instances:missions:challenges:'+self.challenge_type_shortcut+'-fifty-fifty',
                args=(self.game.slug, self.parent.pk, self.pk)
        )


    @property
    def random_answer_choices(self):
        #TODO explain what this is all about
        """ 50/50. generate a list of random....."""

        answers = AnswerChoice.objects.filter(challenge=self)
        try:
            correct_answer = answers.get(is_barrier_correct_answer=True)
        except AnswerChoice.DoesNotExist:
            raise ImproperlyConfigured("A correct answer has not been set on the barrier challenge '%s'" % self.title)

        cnt = 0
        choice_statuses = [False]*answers.count()
        choice_indexes = range(len(choice_statuses))
        while cnt <=  (answers.count()-1)/2:
            random_index = random.choice(choice_indexes)
            if random_index != list(answers).index(correct_answer):
                choice_statuses[random_index] = True
                choice_indexes.pop(random_index)
                cnt+=1
        return choice_statuses

    #def clean(self):
    #    if self.answer_choices.filter(is_barrier_correct_answer=True).count() != 1:
    #        raise ValidationError("Barrier Challenge must have exactly one correct answer set.")

    def save(self, *args, **kwargs):
        #TODO
        # validate to see if the number of points per challenge is not less than
        # minimum_coins_to_play
        if self.challenge_type is None:
            self.challenge_type = Challenge.BARRIER
        super(BarrierChallenge, self).save(*args, **kwargs)

class FinalBarrierChallenge(Challenge):

    def save(self, *args, **kwargs):
        if self.challenge_type is None:
            self.challenge_type = Challenge.FINAL_BARRIER
        super(FinalBarrierChallenge, self).save(*args, **kwargs)

class MapChallenge(Challenge):

    maxNumMarkers = models.IntegerField(default=5)

    class Meta:
        pass

    def save(self, *args, **kwargs):
        if self.challenge_type is None:
            self.challenge_type = Challenge.MAP
        super(MapChallenge, self).save(*args, **kwargs)


class OpenEndedChallenge(Challenge):

    def save(self, *args, **kwargs):
        if self.challenge_type is None:
            self.challenge_type = Challenge.OPEN_ENDED
        super(OpenEndedChallenge, self).save(*args, **kwargs)


class EmpathyChallenge(Challenge):

    def determine_path(instance, filename):
        return 'uploads/empathy_challenges/'+ str(instance.id) +'/'+ filename

    bio_text = models.TextField(verbose_name="Bio", max_length=1000, default='')
    avatar = models.ImageField(upload_to=determine_path, null=True, blank=True)

    @models.permalink
    def get_absolute_url(self):
        return ''

    class Meta:
        pass

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

    is_barrier_correct_answer = models.BooleanField(default=False, verbose_name="Mark this answer as the correct answer")

    objects = AnswerChoiceManager()

    def __unicode__(self):
        return self.value


class ChallengeAnswer(PolymorphicModel):
    """ user submitted answer to a challenge """

    user = models.ForeignKey(User, editable=False, related_name='answers')
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        pass

    @models.permalink
    def get_absolute_url(self):
        return ""


class ChallengeAnswerWithMultipleChoices(ChallengeAnswer):
    """ user submitted response to a multi response challenge """

    selected = models.ManyToManyField(AnswerChoice, related_name='multiresponse_answers')
    challenge = models.ForeignKey(Challenge, related_name='multiresponse_answers')

    #objects = AnswerSingleResponseManager()

    def __unicode__(self):
        return _(u'an answer to %s' % self.challenge)

class ChallengeAnswerWithOneChoice(ChallengeAnswer):
    """ user submitted response to a multi response challenge """

    selected = models.OneToOneField(AnswerChoice, related_name='singleresponse_answers')
    challenge = models.ForeignKey(Challenge, related_name='singleresponse_answers')

    #objects = AnswerSingleResponseManager()

    def __unicode__(self):
        return _(u'an answer to %s' % self.challenge)

class ChallengeAnswerMap(ChallengeAnswer):
    map = GoogleMapsField()
    challenge = models.ForeignKey(MapChallenge, related_name='map_answers')

    #objects = AnswerMapManager()

    def __unicode__(self):
        return _(u'an answer to %s' % self.challenge)

    @models.permalink
    def get_absolute_url(self):
        return ''


class ChallengeAnswerEmpathy(ChallengeAnswer):
    value = models.TextField(verbose_name="Answer Empathy", max_length=1000, default='')
    challenge = models.ForeignKey(EmpathyChallenge, related_name='empathy_answers')

    #objects = AnswerEmpathyManager()

    def __unicode__(self):
        return _(u'an answer to %s' % self.challenge)

    @models.permalink
    def get_absolute_url(self):
        return ""


class ChallengeAnswerOpenEnded(ChallengeAnswer):
    value = models.TextField(verbose_name="Answer Open Ended", max_length=1000, default='')
    challenge = models.ForeignKey(OpenEndedChallenge, related_name='openended_answers')

    #objects = AnswerOpenEndedManager()

    def __unicode__(self):
        return _(u'an answer to %s' % self.challenge)
