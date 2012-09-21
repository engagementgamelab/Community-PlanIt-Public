import os.path
import datetime
from operator import attrgetter
from decimal import Decimal
from uuid import uuid4 as uuid
from cache_utils.decorators import cached

#from stream import utils as stream_utils
from stream.models import Action

from sorl.thumbnail import ImageField

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.urlresolvers import reverse
from django.core.cache import cache
from django.contrib.auth.signals import user_logged_in
from django.utils.translation import ugettext_lazy as _ 

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

from web.instances.models import Instance, Affiliation
from web.missions.models import Mission
#from web.causes.models import PlayerCause
from web.challenges.models import Challenge, BarrierChallenge, Answer

import logging
log = logging.getLogger(__name__)

class UserProfileOptionBase(models.Model):
    pos = models.IntegerField(blank=False, null=False)

    class Meta:
        ordering = ('pos',)
        abstract = True

class UserProfileEducation(UserProfileOptionBase):
    education = models.CharField(max_length=128, blank=True, default='')

    class Meta:
        ordering = ('pos',)
        verbose_name = "User Profile Education option"
        verbose_name_plural = "User Profile Education options"

    def __unicode__(self):
        return self.education

class UserProfileGender(UserProfileOptionBase):
    gender = models.CharField(max_length=128, blank=True, default='')

    class Meta:
        ordering = ('pos',)
        verbose_name = "User Profile Gender option"
        verbose_name_plural = "User Profile Gender options"

    def __unicode__(self):
        return self.gender

class UserProfileHowDiscovered(UserProfileOptionBase):
    how = models.CharField(max_length=128, blank=True, default='')

    class Meta:
        ordering = ('pos',)
        verbose_name = "User Profile How Discovered option"
        verbose_name_plural = "User Profile How Discovered options"

    def __unicode__(self):
        return self.how

class UserProfileIncome(UserProfileOptionBase):
    income = models.CharField(max_length=128, blank=True, default='')

    class Meta:
        ordering = ('pos',)
        verbose_name = "User Profile Income option"
        verbose_name_plural = "User Profile Income options"

    def __unicode__(self):
        return self.income
    
class UserProfileLivingSituation(UserProfileOptionBase):
    situation = models.CharField(max_length=128, blank=True, default='')

    class Meta:
        ordering = ('pos',)
        verbose_name = "User Profile Living Situation option"
        verbose_name_plural = "User Profile Living Situation options"

    def __unicode__(self):
        return self.situation

class UserProfileRace(UserProfileOptionBase):
    race = models.CharField(max_length=128, blank=True, default='')

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
    stake = models.CharField(max_length=128, blank=True, default='')

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

    #@cached(60*60*24, 'user_profile_per_instance_get')
    #def get(self, *args, **kwargs):
    #    return super(UserProfilePerInstanceManager, self).get(*args, **kwargs)

    @cached(60*60*24, 'all_games_for_profile')
    def games_for_profile(self, user_profile):
        game_pks = self.filter(user_profile=user_profile).values_list('instance__pk', flat=True)
        my_games = Instance.objects.filter(pk__in=game_pks)
        return my_games

    # deprecated. points now come from the core.PlayerLeaderboard
    #@cached(60*60*24)
    #def total_points_for_profile(self, instance, user_profile):
    #    log.debug("profile manager: total_points_for_profile %s ** not cached **" % user_profile.screen_name)
    #    try:
    #        return self.get(instance=instance, user_profile=user_profile).total_points
    #    except UserProfilePerInstance.DoesNotExist:
    #        return 0

    #@cached(60*60*24, 'progress_data_for_mission')
    def progress_data_for_mission(self, instance, mission, user_profile):
        return self.get(instance=instance, user_profile=user_profile).\
                progress_percentage_by_mission(mission)

    #def latest_instance_by_profile(self, user_profile, domain):
    #    return self.objects.filter(user_profile=user_profile).latest_for_city_domain(domain)

    #def total_points_by_affiliation(self, instance, affiliation_slug):
    #    total_points = 0
    #    for player_profile in self.all_by_affiliation(instance, affiliation_slug):
    #        total_points+=self.total_points_for_profile(instance, player_profile)
    #    return total_points

class UserProfilePerInstance(models.Model):
    user_profile = models.ForeignKey("UserProfile", related_name='user_profiles_per_instance')
    instance = models.ForeignKey(Instance)

    # to be removed
    stake = models.ForeignKey(UserProfileStake, blank=True, null=True, default=None)

    stakes = models.ManyToManyField(UserProfileStake, blank=True, null=True, related_name='stakes')
    affils = models.ManyToManyField(Affiliation, blank=True, null=True, related_name='user_profiles_per_instance')

    date_created = models.DateTimeField(auto_now_add=True)

    objects = UserProfilePerInstanceManager()

    def __unicode__(self):
        return "%s's profile" % (self.user_profile.screen_name)

    @models.permalink
    def get_absolute_url(self):
        return ('accounts:player_profile', [str(self.get_user().pk)])

    class Meta:
        unique_together = ('user_profile', 'instance',)
        ordering = ('date_created', 'user_profile__user__last_name', )

    def progress_percentage_by_mission(self, mission):
        mission_total_points = mission.total_points
        my_completed = self.my_completed_by_mission(mission)
        # not displaying points for mission anymore. see
        # base_city.html
        my_points_for_mission = 0 #self.total_points_by_mission(mission)
        percentage = int(my_points_for_mission/mission_total_points*Decimal(100))
        return (my_points_for_mission, percentage)

    def get_user(self):
        @cached(60*60*24*30)
        def this_user(pk):
            return self.user_profile.user
        return this_user(self.pk)

    @property
    def badges(self):
        return BadgePerPlayer.objects.filter(user=self.get_user)

    def my_last_login_from_stream(self):
        """
            get the latest login from activity stream 
            return the datetime 
        """
        return Action.objects.get_for_actor(self.get_user()).filter(verb='user_logged_in').latest('datetime')

    #@property
    #def format_stakes(self):
    #    return ", ".join(self.stakes.language(get_language()).all().values_list('stake', flat=True))

    @property
    def user_profile_email(self):
        return self.user_profile.email or self.user_profile.user.email 

#stream_utils.register_target(UserProfilePerInstance)


class PlayerMissionStateManager(models.Manager):

    def by_game(self, game):
        return self.filter(mission__parent=game)

    def total_coins_by_mission(self, profile_per_instance, mission):
        return  self.filter(profile_per_instance=profile_per_instance, mission=mission).\
                                    aggregate(models.Sum('coins')).get('coins__sum') or 0

        self.by_game(game)
    def total_coins_by_game(self, profile_per_instance, game):
        self.by_game(game)



class PlayerMissionState(models.Model):
    """ keep track of mission state for each player """

    mission = models.ForeignKey(Mission, related_name='player_mission_states')
    challenges_locked = models.ManyToManyField(Challenge, blank=True, null=True, related_name='challenges_locked')
    challenges_unlocked = models.ManyToManyField(Challenge, blank=True, null=True, related_name='challenges_unlocked')
    challenges_completed = models.ManyToManyField(Challenge, blank=True, null=True, related_name='challenges_completed')
    barriers_fifty_fifty = models.ManyToManyField(Challenge, blank=True, null=True, related_name='barriers_fifty_fifty')
    coins = models.IntegerField(default=0)

    objects = PlayerMissionStateManager()

    def init_state(self):
        """ called after creation from MissionListView to initialize state"""
        self.challenges_unlocked.clear()
        self.challenges_locked.clear()
        self.challenges_completed.clear()
        self.coins = 0

        for i, barrier in enumerate(self.mission.challenges_as_sorteddict):
            if i == 0:
                self.challenges_unlocked.add(barrier)
                for challenge in self.mission.challenges_as_sorteddict.get(barrier):
                    self.challenges_unlocked.add(challenge)
            else:
                self.challenges_locked.add(barrier)
                for challenge in self.mission.challenges_as_sorteddict.get(barrier):
                    self.challenges_locked.add(challenge)
        self.save()

    def unlock_next_block(self):
        """ a barrier has been completed. unlock next block of challenges"""
        for i, barrier in enumerate(self.mission.challenges_as_sorteddict):
            if not barrier in self.challenges_completed.all():
                for challenge in self.mission.challenges_as_sorteddict.get(barrier):
                    self.challenges_unlocked.add(challenge)
                    self.challenges_locked.remove(challenge)

    @property
    def next_barrier(self):
        for barrier in Challenge.objects.filter(parent=self.mission).\
                instance_of(BarrierChallenge):
            if barrier.basetreenode_ptr.get_previous_sibling().get_real_instance() in \
                    self.challenges_unlocked.all():
                return barrier


class UserProfile(models.Model):

    def determine_path(instance, filename):
        return os.path.join('uploads', 'avatars', str(instance.user.id), filename)


    user = models.ForeignKey(User, unique=True)
    instances = models.ManyToManyField(Instance, blank=True, null=True, related_name='user_profiles', through=UserProfilePerInstance)
    mission_states = models.ManyToManyField(PlayerMissionState, related_name='user_profiles', blank=True, null=True)

    avatar = ImageField(upload_to=determine_path, null=True, blank=True)
    email = models.EmailField(_('e-mail address'), blank=True, max_length=250)
    receive_email = models.BooleanField(default=True)
    city = models.CharField(max_length=128, blank=True, default='')
    zip_code = models.CharField(max_length=10, blank=True, default='')

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

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __unicode__(self):
        return "%s's profile" % (self.screen_name)

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
        return ('accounts:player_profile', [str(self.user.id)])

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



@receiver(post_save, sender=Answer)
def update_player_mission_state(sender, **kwargs):
    answer = kwargs.get('instance')

    if  kwargs.get('created') == True and \
            isinstance(answer, Answer):

        challenge = answer.challenge
        mission = challenge.parent
        user_profile = answer.user.get_profile()
        player_mission_state = user_profile.mission_states.get(mission=mission)

        # append to the completed challenges
        player_mission_state.challenges_completed.add(challenge)
        # increment the coins count for non-barrier challenges
        if challenge.challenge_type != Challenge.BARRIER:
            player_mission_state.coins += mission.challenge_coin_value
        # if barrier has been played, unlock next block of challenges
        if challenge.challenge_type == Challenge.BARRIER:
            # if chosen answer is incorrect, subtract coins
            if answer.selected.is_barrier_correct_answer != True:
                player_mission_state.coins -= mission.challenge_coin_value
            player_mission_state.unlock_next_block()

        # if the next barrier in order is eligible to be unlocked
        # add it to the challenges_unlocked
        #next_barrier = player_mission_state.next_barrier
        #if next_barrier.minimum_coins_to_play <= player_mission_state.coins:
        #     player_mission_state.challenges_unlocked.add(next_barrier)
        #     player_mission_state.challenges_locked.remove(next_barrier)

        player_mission_state.save()
post_save.connect(update_player_mission_state, dispatch_uid='update_mission_state')


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

#stream_utils.register_actor(User)

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

    latest req. 05-05-2012

        -- When someone likes their comment or response.
        -- when someone replies to their comment or response
        -- when someone joins their get together
        -- when someone comments on their profile
        -- when someone completes a challenge they posed.
        -- when they earn a badge
        -- when they earn a flag
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

    def __unicode__(self):
        return "notification for %s" % (self.user.get_profile().screen_name)

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

#Deprecated
#capturing the login in accounts.views.login_ajax
#def capture_user_login(sender, user, request, dispatch_uid='user_logins', **kwargs):
# TODO
#   somehow capture the game the user
#   is logging into
#    stream_utils.action.send(
#                    actor=user,
#                    verb='user_logged_in',
#                    #target=request.current_game,
#                    description='user logged in to system'
#    )
#user_logged_in.connect(capture_user_login)
