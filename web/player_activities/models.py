import datetime

from django.core.urlresolvers import reverse
from django.db import models

from django.contrib.auth.models import User
from django.contrib.contenttypes import generic

from nani.models import TranslatableModel, TranslatedFields

from web.accounts.models import determine_path
from web.attachments.models import Attachment
from web.comments.models import Comment
from web.missions.models import Mission


__all__ = ( 'PlayerActivityType','PlayerActivity', 'PlayerMapActivity', 'PlayerEmpathyActivity', 'MultiChoiceActivity', )

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
        return self.safe_translation_getter('name', '%s' % self.pk)

    def save(self, *args, **kwargs):
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

    def __unicode__(self):
        return self.safe_translation_getter('name', '%s' % self.pk)

    def save(self, *args, **kwargs):
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

    def __unicode__(self):
        return self.safe_translation_getter('value', '%s' % self.bio[:10])

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
        return '%s' % self.pk # self.safe_translation_getter('value', '%s' % self.pk)

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
