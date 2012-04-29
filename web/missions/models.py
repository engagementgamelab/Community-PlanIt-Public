import datetime
from decimal import Decimal
from operator import attrgetter
from dateutil.relativedelta import relativedelta
from stream import utils as stream_utils
from stream.models import Action
from django.template.defaultfilters import slugify
from django.db import models
from django.contrib import admin
from django.db.models import Q

from nani.models import TranslatableModel, TranslatedFields
from nani.manager import TranslationManager

from web.instances.models import Instance

import logging
log = logging.getLogger(__name__)

class MissionManager(TranslationManager):

    def latest_by_instance(self, instance):
        missions_for_instance = self.filter(instance=instance)
        if missions_for_instance:
            latest_by =  max(missions_for_instance.values_list('end_date', flat=True))
            return self.get(**dict(end_date=latest_by))

        return self.none()

    def past(self, instance=None):
        kwargs = dict(end_date__lt=datetime.datetime.now(),)
        if instance:
            kwargs.update(dict(instance=instance))
        return self.filter(**kwargs).order_by('-end_date')

    def future(self, instance=None):
        kwargs = dict(start_date__gt=datetime.datetime.now(),)
        if instance:
            kwargs.update(dict(instance=instance))
        return self.filter(**kwargs).order_by('start_date')

    def active(self, instance=None):
        now = datetime.datetime.now()
        kwargs = dict(start_date__lte=now, end_date__gte=now,)
        if instance:
            kwargs.update(dict(instance=instance))
        return self.filter(**kwargs).order_by('start_date')


class Mission(TranslatableModel):

    # percentage for total points per mission
    # earned toward a mission flag 
    MISSION_FLAG_PERCENTAGE = 80

    title = models.CharField(max_length=255, verbose_name="Title (non-translatable)")
    instance = models.ForeignKey(Instance, related_name='missions')
    slug = models.SlugField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    video = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    translations = TranslatedFields(
        name = models.CharField(max_length=255, blank=True),
        description = models.TextField(blank=True),
        #meta = {'get_latest_by': 'start_date'}
    )

    objects = MissionManager()

    class Meta:
    	ordering = ('end_date',)
        #get_latest_by = 'start_date'

    @models.permalink
    def get_absolute_url(self):
        return ('missions:mission', [self.slug])

    @property
    def ends_in_days(self):
        delta =  self.end_date - datetime.datetime.now()
        return delta.days
        
    @property
    def starts_in_days(self):
        delta = self.start_date - datetime.datetime.now()
        return delta.days

    def is_active(self):
        now = datetime.datetime.now()
        return self.start_date <= now and now <= self.end_date

    def is_expired(self):
        return datetime.datetime.now() > self.end_date

    @property
    def is_started(self):
        return datetime.datetime.now() >= self.start_date

    @property
    def is_future(self):
        return datetime.datetime.now() <= self.start_date

    @property
    def total_points(self):
        return Decimal(sum([activity.get_points() for activity in self.get_activities()]))

    #@property
    #def mission_flag_points(self):
    #    return self.total_points / Decimal(Mission.MISSION_FLAG_PERCENTAGE)*Decimal(100)

    #def total_points_for_completed_activities(self, user):

    #def get_completed_activities_count(self, user=None):
    #    return self.completed_from_stream.count()

    #def completed_from_stream(self, user=None):
    #    """ return a QuerySet of Action instances of completed activities """
    #    for_mission = self.get_activities()
    #    qs = Action.objects.filter(
    #            verb = 'activity_completed'
    #    ).filter(
    #            Q(action_object_playeractivity__in=for_mission) | 
    #            Q(action_object_playermapactivity__in=for_mission) | 
    #            Q(action_object_playerempathyactivity__in=for_mission)
    #    )
    #    if user:
    #        qs = qs.filter(actor_user=user)
    #    return qs

    #def get_completed_by_user(self, user):
    #    all_activities = self.get_activities()
    #    completed_from_stream = self.completed_from_stream(user)

    def get_activities(self):
        """ return a list of all available activities """
        activities = []
        for model_klass in ['PlayerActivity', 'PlayerEmpathyActivity', 'PlayerMapActivity']:
            activities.extend(getattr(self, 'player_activities_%s_related' % model_klass.lower()).all())
        return sorted(activities, key=attrgetter('name'))

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)[:50]
        if not self.start_date and not self.end_date:
            latest = Mission.objects.latest_by_instance(self.instance)
            if latest:
                self.start_date = latest.end_date
                self.end_date = latest.end_date + relativedelta(days=+self.instance.days_for_mission+1, hour=0, minute=0, second=0)
            else:
                self.start_date = datetime.datetime.now()
                self.end_date = self.start_date + relativedelta(days=+self.instance.days_for_mission+1, hour=0, minute=0, second=0)

        super(Mission, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

stream_utils.register_target(Mission)


