__all__ = (
        'Answer', 'AnswerSingleResponse', 'AnswerOpenEnded', 'AnswerMap', 'AnswerEmpathy', 'AnswerMultiChoice'
)

import datetime
from cache_utils.decorators import cached

from django.db import models
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.utils.translation import gettext as _

from django.contrib.auth.models import User
from django.contrib.contenttypes import generic

from gmapsfield.fields import GoogleMapsField

from web.comments.models import Comment
from web.missions.models import Mission
from web.player_activities.models import *

class Answer(models.Model):
    answerUser = models.ForeignKey(User, editable=False, related_name='answers')
    comments = generic.GenericRelation(Comment)
    createDate = models.DateTimeField(editable=False)

    class Meta:
        ordering = ('-createDate',)

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
    activity = models.ForeignKey(PlayerActivity, related_name='singleresponse_answers')

    objects = AnswerSingleResponseManager()

    def __unicode__(self):
        return _(u'an answer to %s' % self.activity)


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
    activity = models.ForeignKey(PlayerMapActivity, related_name='map_answers')

    objects = AnswerMapManager()

    def __unicode__(self):
        return _(u'an answer to %s' % self.activity)

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
    activity = models.ForeignKey(PlayerEmpathyActivity, related_name='empathy_answers')

    objects = AnswerEmpathyManager()

    def __unicode__(self):
        return _(u'an answer to %s' % self.activity)

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
    activity = models.ForeignKey(PlayerActivity, related_name='openended_answers')

    objects = AnswerOpenEndedManager()

    def __unicode__(self):
        return _(u'an answer to %s' % self.activity)

