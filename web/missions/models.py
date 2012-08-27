import os.path
from datetime import datetime, timedelta
from decimal import Decimal
from operator import attrgetter

from model_utils.managers import InheritanceManager
from cache_utils.decorators import cached
from stream import utils as stream_utils

from django.conf import settings
from django.core.cache import cache
#from django.db.models.signals import post_save
from django.db import models
from django.contrib import admin

from web.instances.models import Instance, BaseTreeNode
from web.challenges.models import Challenge

import logging
log = logging.getLogger(__name__)

"""
class MissionManager(TreeManager):

    @cached(60*60*24, 'missions_for_instance')
    def for_instance(self, instance):
        return self.filter(instance=instance)

    @cached(60*60*24, 'missions')
    def latest_by_instance(self, instance):
        missions_for_instance = self.filter(instance=instance)
        if missions_for_instance:
            latest_by =  max(missions_for_instance.values_list('end_date', flat=True))
            return self.get(**dict(end_date=latest_by))

        return self.none()

    @cached(60*60*24, 'missions')
    def past(self, instance):
        return self.filter(instance=instance, end_date__lt=datetime.datetime.now()).order_by('-end_date')

    @cached(60*60*24, 'missions')
    def future(self, instance):
        return self.filter(instance=instance, start_date__gt=datetime.datetime.now()).order_by('start_date')

    #@cached(60*60*24, 'missions')
    def default(self, instance_id):
        qs =  self.active(instance_id)
        if qs.count() > 0:
            return qs[0]

    def first(self, instance_id):
        qs =  self.filter(instance__pk=instance_id).order_by('start_date')
        if qs.count() > 0:
            return qs[0]

    #@cached(60*60*24, 'missions')
    def active(self, instance_id):
        now = datetime.datetime.now()
        qs = self.filter(instance__pk=instance_id, start_date__lte=now, end_date__gte=now).order_by('start_date')
        return qs
"""


class Mission(BaseTreeNode):

    description = models.TextField(blank=True)
    video = models.TextField(blank=True)
    challenge_coin_value = models.IntegerField(verbose_name="coin value for challenge", default=0)
    created_date = models.DateTimeField(auto_now_add=True)

    #objects = MissionManager()

    @property 
    def start_date(self):
        for dt, m in self.parent._missions_by_start_date.\
                iteritems():
            if m == self:
                return dt

    @property 
    def end_date(self):
        return self.start_date + \
            timedelta(days=self.parent.days_for_mission)

    @property
    def ends_in_days(self):
        delta =  self.end_date - datetime.now()
        return delta.days

    @property
    def starts_in_days(self):
        delta = self.start_date - datetime.now()
        return delta.days

    @property
    def is_active(self):
        return self == self.parent.active_mission

    @property
    def is_expired(self):
        return datetime.now() > self.end_date

    @property
    def is_future(self):
        return datetime.now() <= self.start_date

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('missions:mission', (), {
            'mission_id': self.pk
        })

    def get_next_mission(self):
        return self.get_next_sibling()

    def get_previous_mission(self):
        return self.get_previous_sibling()

    @property
    def initial_challenges(self):
        initial_unlocked = []
        #for challenge in map(lambda c: c.get_real_instance(), 
        #        self.get_children()):
        for challenge in Challenge.objects.filter(parent=self):
            if challenge.challenge_type != Challenge.BARRIER:
                initial_unlocked.append(challenge)
            else:
                return initial_unlocked


stream_utils.register_target(Mission)

#ALTER TABLE stream_action ADD COLUMN action_object_mission_id integer;
stream_utils.register_action_object(Mission)

# invalidate cache for 'missions' group
def invalidate_mission(sender, **kwargs):
    activity = kwargs.pop('instance')
    if activity:
        mission_id = activity.mission.pk
        Mission.get_challenges_cached.invalidate(mission_id)
        Mission.get_player_submitted_activities_cached.invalidate(mission_id)

#post_save.connect(invalidate_mission, Mission)
#post_save.connect(invalidate_prof_per_instance, Mission)

#def invalidate_activities_for_mission(sender, **kwargs):
#    activity = kwargs.get('instance')
#    log.debug("on_delete. invaliding activities_for_mission %s" %  activity)
#    Mission.objects.activities_for_mission(slug=activity.mission.slug)

