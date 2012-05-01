import os.path
import datetime
from decimal import Decimal
from uuid import uuid4 as uuid
from cache_utils.decorators import cached

from stream import utils as stream_utils
from stream.models import Action

from django import forms
from django.core.urlresolvers import reverse
from django.core.cache import cache
from django.contrib.auth.signals import user_logged_in
from django.db import models
from django.utils.translation import get_language, ugettext_lazy as _ 

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

from nani.models import TranslatableModel, TranslatedFields

from web.comments.models import Comment
from web.accounts.models import *
from web.challenges.models import *
from web.instances.models import Instance, Affiliation
from web.missions.models import Mission

import logging
log = logging.getLogger(__name__)

class UserProfileOptionBase(TranslatableModel):
    pos = models.IntegerField(blank=False, null=False)

    class Meta:
        ordering = ('pos',)
        abstract = True

class UserProfileEducation(UserProfileOptionBase):
    translations = TranslatedFields(
        education = models.CharField(max_length=128)
    )

    class Meta:
        ordering = ('pos',)
        verbose_name = "User Profile Education option"
        verbose_name_plural = "User Profile Education options"

    def __unicode__(self):
        return self.education

class UserProfileGender(UserProfileOptionBase):
    translations = TranslatedFields(
        gender = models.CharField(max_length=128)
    )

    class Meta:
        ordering = ('pos',)
        verbose_name = "User Profile Gender option"
        verbose_name_plural = "User Profile Gender options"

    def __unicode__(self):
        return self.gender

class UserProfileHowDiscovered(UserProfileOptionBase):
    translations = TranslatedFields(
        how = models.CharField(max_length=128)
    )

    class Meta:
        ordering = ('pos',)
        verbose_name = "User Profile How Discovered option"
        verbose_name_plural = "User Profile How Discovered options"

    def __unicode__(self):
        return self.how

class UserProfileIncome(UserProfileOptionBase):
    translations = TranslatedFields(
        income = models.CharField(max_length=128)
    )

    class Meta:
        ordering = ('pos',)
        verbose_name = "User Profile Income option"
        verbose_name_plural = "User Profile Income options"

    def __unicode__(self):
        return self.income
    
class UserProfileLivingSituation(UserProfileOptionBase):
    translations = TranslatedFields(
        situation = models.CharField(max_length=128)
    )

    class Meta:
        ordering = ('pos',)
        verbose_name = "User Profile Living Situation option"
        verbose_name_plural = "User Profile Living Situation options"

    def __unicode__(self):
        return self.situation

class UserProfileRace(UserProfileOptionBase):
    translations = TranslatedFields(
        race = models.CharField(max_length=128)
    )

    class Meta:
        ordering = ('pos',)
        verbose_name = "User Profile Race option"
        verbose_name_plural = "User Profile Race options"

    def __unicode__(self):
        return self.race

class UserProfileStake(UserProfileOptionBase):
    """
    The stakes users hold in the community, e.g. Live, Work, Play, or Teacher,
    Administrator, Student.
    """
    translations = TranslatedFields(
        stake = models.CharField(max_length=128),
    )

    class Meta:
        ordering = ('pos',)
        verbose_name = "User Profile Stake option"
        verbose_name_plural = "User Profile Stake options"

    def __unicode__(self):
        return self.stake

class CPIUser(User):

    class Meta:
        proxy = True

    def __unicode__(self):
        if self.first_name and self.last_name:
            return "%s %s" % (self.first_name, self.last_name)
        return self.username

class UserProfilePerInstanceManager(models.Manager):

    @cached(60*60*24, 'user_profile_per_instance_get')
    def get(self, *args, **kwargs):
        log.debug('get prof_per_instance %s ** no cache **' % kwargs)
        return super(UserProfilePerInstanceManager, self).get(*args, **kwargs)

    @cached(60*60*24, 'all_games_for_profile')
    def games_for_profile(self, user_profile):
        game_pks = self.filter(user_profile=user_profile).values_list('instance__pk', flat=True)
        my_games = Instance.objects.filter(pk__in=game_pks)
        log.debug('my games %s. ** no cached ** ' % my_games)
        return my_games

    #def latest_instance_by_profile(self, user_profile, domain):
    #    return self.objects.filter(user_profile=user_profile).latest_for_city_domain(domain)

class UserProfilePerInstance(models.Model):
    user_profile = models.ForeignKey("UserProfile", related_name='user_profiles_per_instance')
    instance = models.ForeignKey(Instance)

    # to be removed
    stake = models.ForeignKey(UserProfileStake, blank=True, null=True, default=None)

    stakes = models.ManyToManyField(UserProfileStake, blank=True, null=True, related_name='stakes')
    affils = models.ManyToManyField(Affiliation, blank=True, null=True, related_name='affiliations')

    date_created = models.DateTimeField(auto_now_add=True)

    objects = UserProfilePerInstanceManager()

    def __unicode__(self):
        return "'%s <%s>' for: %s" % (self.user_profile.user.get_full_name(), self.user_profile.email, self.instance.title, )

    def progress_percentage_by_mission(self, mission):
        # TODO
        # this cache group gets invalidated explicitly for everybody 
        # as a challenge is played.
        # update to only invalidate for this pk and mission 
        @cached(60*60*24, 'my_progress_data')
        def my_progress(pk, mission):
            log.debug("running progress_percentage_by_mission ** not cached ** ")
            mission_total_points = mission.total_points
            my_completed = self.my_completed_by_mission(mission)
            my_points_for_mission = Decimal(sum(activity.get_points() for activity in my_completed))
            percentage = int(my_points_for_mission/mission_total_points*Decimal(100))
            log.debug("%s/%s (%s percent). %s" % (
                                                my_points_for_mission,
                                                mission_total_points,
                                                percentage,
                                                mission.title,
                                                )
            )
            return (my_points_for_mission, percentage)
        return my_progress(self.pk, mission)

    def get_user(self):
        @cached(60*60*24*30)
        def this_user(pk):
            log.debug("got user for profile **no cache**")
            return self.user_profile.user
        return this_user(self.pk)

    @property
    def total_points(self):
        my_completed = []
        for mission in Mission.objects.for_instance(self.instance):
            my_completed.extend(self.my_completed_by_mission(mission))
        return Decimal(sum(activity.get_points() for activity in my_completed))

    def my_completed_by_mission(self, mission):
        def activities_from_actions(actions):
            return [getattr(action, 'action_object_playeractivity') or \
                    getattr(action, 'action_object_playermapactivity') or \
                    getattr(action, 'action_object_playerempathyactivity') for action in actions]
        activities_for_mission = mission.get_activities()
        if len(activities_for_mission) == 0:
            return []
        # do not pass en empty list to Action.get_for_action_objects
        # it will blow up
        actions = Action.objects.get_for_action_objects(activities_for_mission)
        actions_completed_activities = filter(lambda a: a.verb == "activity_completed" and a.actor==self.get_user(), actions)
        return activities_from_actions(actions_completed_activities)

    @property
    def flags(self):
        all_missions_for_game = Mission.objects.filter(instance=self.instance)
        my_flags = all_missions_for_game.count()

        for m in all_missions_for_game:
            min_points_for_mission = Decimal(m.total_points) * (Decimal(Mission.MISSION_FLAG_PERCENTAGE) / Decimal(100))
            my_completed = self.my_completed_by_mission(m)
            my_points_for_mission = Decimal(sum(activity.get_points() for activity in my_completed))
            if my_points_for_mission > min_points_for_mission:
                my_flags+=1
        return my_flags

    @property
    def format_stakes(self):
        return ", ".join(self.stakes.language(get_language()).all().values_list('stake', flat=True))

    @property
    def user_profile_email(self):
        return self.user_profile.email or self.user_profile.user.email 

    class Meta:
        unique_together = ('user_profile', 'instance',)
        ordering = ('date_created', 'user_profile__user__last_name', )

def determine_path(instance, filename):
    return os.path.join('uploads', 'avatars', str(instance.user.id), filename)

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    instances = models.ManyToManyField(Instance, blank=True, null=True, related_name='user_profiles_list', through=UserProfilePerInstance)

    avatar = models.ImageField(upload_to=determine_path, null=True, blank=True)
    email = models.EmailField(_('e-mail address'), blank=True, max_length=250)
    receive_email = models.BooleanField(default=True)
    city = models.CharField(max_length=128, blank=True, default='')
    zip_code = models.CharField(max_length=10, blank=True, default='')
    preferred_language = models.CharField(max_length=5, default='en-us')

    # Additional profile fields
    birth_year = models.IntegerField(blank=True, null=True, default=0)
    gender = models.ForeignKey(UserProfileGender, blank=True, null=True, default=None)
    race = models.ForeignKey(UserProfileRace, blank=True, null=True, default=None)
    education = models.ForeignKey(UserProfileEducation, blank=True, null=True, default=None)
    income = models.ForeignKey(UserProfileIncome, blank=True, null=True, default=None)
    living = models.ForeignKey(UserProfileLivingSituation, blank=True, null=True, default=None)
    how_discovered = models.ForeignKey(UserProfileHowDiscovered, blank=True, null=True, default=None)
    how_discovered_other = models.CharField(max_length=1000, blank=True, default='')
    tagline = models.CharField(max_length=140, blank=True, default='')

    #
    # internal system records
    #
    # the current number of coins that the player has
    currentCoins = models.IntegerField(default=0)
    # the total points that the player has accrued
    totalPoints = models.IntegerField(default=0)
    # points to the next coin
    coinPoints = models.IntegerField(default=0)
    # comments on the profile from others
    comments = generic.GenericRelation(Comment)

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __unicode__(self):
        return "%s's profile <%s>" % (self.screen_name, self.user.email)

    #@property
    #def active_instance(self):
    #    profiles_per_instance = UserProfilePerInstance.objects.filter(user_profile=self)
    #    if profiles_per_instance.count():
    #        return profiles_per_instance[0].instance

    @property
    def affiliations_csv(self):
        if self.affils:
            return self.affils.values_list('name', flat=True)
        return ""

    def earned_tokens(self):
        return self.totalPoints // 100

    @models.permalink
    def get_absolute_url(self):
        return ('accounts_profile', [str(self.user.id)])

    def points_progress(self):
        return self.coinPoints

    def points_to_coin(self):
        return 100 - self.coinPoints
    
    def points_to_coin_for_fill(self):
        return self.coinPoints

    @property
    def screen_name(self):
        #First name and last name are required
        first = self.user.first_name or ''
        if first and len(first) > 1:
            first = first[0].upper() + first[1:]

        last = self.user.last_name or ''
        if last:
            if len(last) > 1:
                last = last[0].upper() + last[1:]
                last = "%s." % last[0]
            else:
                last = last[0]

        if first or last:
            return "%s %s" % (first, last)

        return self.user.username

class UserProfileVariantsForInstance(models.Model):
    instance = models.OneToOneField(Instance, unique=True, related_name='user_profile_variants')
    stake_variants = models.ManyToManyField(UserProfileStake, blank=True, null=True, default=None)
    affiliation_variants = models.ManyToManyField(Affiliation, blank=True, null=True, default=None)


# Custom hook for adding an anonymous username to the User model.
def user_pre_save(instance, **kwargs):
    if not instance.username:
        instance.username = str(uuid().hex)[:30]

# Custom post save hook for adding group and user profile
def user_post_save(instance, created, **kwargs):
    if created:
        # Create a user profile for the player and add them to the
        # `Player` group.  Default the player to inactive.
        player_group, created = Group.objects.get_or_create(name='Player')
        user_profile = UserProfile.objects.get_or_create(user=instance)
        #instance.is_active = False
        #instance.groups.add(player_group)
        instance.save()

models.signals.pre_save.connect(user_pre_save, sender=User)
models.signals.post_save.connect(user_post_save, sender=User)

stream_utils.register_actor(User)

class NotificationQueryMixin(object):
    def unread(self):
        return self.filter(read=False)

class NotificationQuerySet(models.query.QuerySet, NotificationQueryMixin):
    pass

class NotificationManager(models.Manager, NotificationQueryMixin):
    def get_query_set(self):
        return NotificationQuerySet(self.model, using=self._db)

class Notification(models.Model):
    """
    These notifications are messages for a particular user, sent by the system
    when another user likes or replies to a comment, or completes a challenge.
    """
    timestamp = models.DateTimeField(default=datetime.datetime.now)
    user = models.ForeignKey(User, related_name='notifications')
    message = models.TextField()
    read = models.BooleanField(default=False)

    # notifications can be sent for any model
    content_type  = models.ForeignKey(ContentType,
                                      blank=True, null=True,
                                      verbose_name=_('content type'),
                                      related_name="content_type_set_for_%(class)s"
                                     )
    object_id      = models.TextField(_('object ID'), blank=True)
    content_object = generic.GenericForeignKey()

    objects = NotificationManager()

    class Meta:
        ordering = ['-timestamp']

    def get_content_object_url(self):
        """
        Return the URL of the object associated with the notification.
        """
        return self.content_object.get_absolute_url()


# invalidate cache for 'prof_per_instance' group
#def invalidate_prof_per_instance(sender, **kwargs):
#    log.debug("invalidating cache for group `prof_per_instance` ")
#    cache.invalidate_group('prof_per_instance')

def capture_user_login(sender, user, request, **kwargs):
    # TODO
    #   somehow capture the game the user
    #   is logging into
    stream_utils.action.send(
                    actor=user,
                    verb='user_logged_in',
                    #target=request.current_game,
                    description='user logged in to system'
    )
user_logged_in.connect(capture_user_login)
