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
from django.db.models import Q
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.urlresolvers import reverse
from django.core.cache import cache
from django.contrib.auth.signals import user_logged_in
from django.utils.translation import ugettext_lazy as _ 

from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

from web.instances.models import Instance, Affiliation
from web.missions.models import Mission
#from web.causes.models import PlayerCause
from web.challenges.models import Challenge, BarrierChallenge, Answer

from .options import *
from .managers import UserProfilePerInstanceManager, PlayerMissionStateManager


import logging
log = logging.getLogger(__name__)



class CPIUser(User):

    class Meta:
        proxy = True

    def __unicode__(self):
        if self.first_name and self.last_name:
            return "%s %s" % (self.first_name, self.last_name)
        return self.username



class UserProfilePerInstance(models.Model):
    user_profile = models.ForeignKey("UserProfile", related_name='user_profiles_per_instance')
    instance = models.ForeignKey(Instance)

    stakes = models.ManyToManyField(UserProfileStake, blank=True, null=True, related_name='stakes')
    affils = models.ManyToManyField(Affiliation, verbose_name = "Affiliations", blank=True, null=True, related_name='user_profiles_per_instance')

    date_created = models.DateTimeField(auto_now_add=True)

    objects = UserProfilePerInstanceManager()

    def __unicode__(self):
        return "%s's profile" % (self.user_profile.screen_name)

    @models.permalink
    def get_absolute_url(self):
        return ('accounts:player_profile', [str(self.get_user().pk)])

    class Meta:
        verbose_name = "Game specific info"
        verbose_name_plural = "Game specific info"
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


class PlayerMissionState(models.Model):
    """ keep track of mission state for each player 

        currently an instance of this model is created by
            `accounts.mixins.PlayerMissionStateContextMixin`
        `PlayerMissionStateManager.create` method assigns 
        the state of challanges (locked/unlocked)

    """

    user = models.ForeignKey(User, verbose_name=_('user'), related_name="mission_states")
    mission = models.ForeignKey(Mission, related_name='mission_states')
    #locked = models.ManyToManyField(Challenge, blank=True, null=True, related_name='challenges_locked')
    #unlocked = models.ManyToManyField(Challenge, blank=True, null=True, related_name='challenges_unlocked')
    #completed = models.ManyToManyField(Challenge, blank=True, null=True, related_name='challenges_completed')
    #barriers_fifty_fifty = models.ManyToManyField(Challenge, blank=True, null=True, related_name='barriers_fifty_fifty')

    locked = models.CommaSeparatedIntegerField(max_length=200, blank=True, default='')
    unlocked = models.CommaSeparatedIntegerField(max_length=200, blank=True, default='')
    completed = models.CommaSeparatedIntegerField(max_length=200, blank=True, default='')
    barriers_fifty_fifty = models.CommaSeparatedIntegerField(max_length=200, blank=True, default='')

    coins = models.IntegerField(default=0)

    objects = PlayerMissionStateManager()

    def __unicode__(self):
        return "Mission: %s, %s unlocked, %s locked, %s completed, %s coins" %(
                                            self.mission.__unicode__(),
                                            len(self.unlocked.split(',')),
                                            len(self.locked.split(',')),
                                            len(self.completed.split(',')),
                                            self.coins,)
        return "player mission state..."

    class Meta:
        unique_together = ('mission', 'user')

    #def state_as_str(self, state_name):
    #    return str(state).replace('[', '').replace(']', '')

    def csvfield_as_list(self, fld_value):
        if ',' in fld_value:
            return map(lambda x: int(x.strip()), fld_value.split(','))
        return []

    def update_challenge_state(self, action, fld, id):
        fld_value = getattr(self, fld)
        print fld, "before update: ", fld_value
        state_list = self.csvfield_as_list(fld_value)
        if action == 'add':
            state_list.append(id)
            print 'added to %s %s' %(fld, id)

        if action == 'remove':
            state_list.remove(id)
            print 'removed to %s %s' %(fld, id)

        setattr(self, fld, str(state_list).replace('[', '').replace(']', ''))
        print fld, "after update: ", getattr(self, fld)

    def all_x_foos(self, fld_name, val):
        val = str(val)
        kw1 = {'{0}__startswith'.format(fld_name) : val+','}
        kw2 = {'{0}__endswith'.format(fld_name) : val+','}
        kw3 = {'{0}__contains'.format(fld_name) : ',{0},'.format(val)}
        kw4 = {'{0}__exact'.format(fld_name) : val}
        return PlayerMissionState.objects.filter(
                Q(**kw1) | Q(**kw2) | Q(**kw3) | Q(**kw4)
        )

    def init_state(self):

        sorted_challenges = self.mission.challenges_as_sorteddict
        self.locked = self.unlocked = self.completed = u''
        for i, barrier in enumerate(sorted_challenges):
            if i == 0:
                # Lock the first barrier
                # The rule for a barrier to be unlocked
                # is to earn 3x the coins per one challenge
                self.update_challenge_state('add', 'locked', barrier.pk)
                for challenge in sorted_challenges.get(barrier):
                    self.update_challenge_state('add', 'unlocked', challenge.pk)
            else:
                self.update_challenge_state('add', 'locked', barrier.pk)
                for challenge in sorted_challenges.get(barrier):
                    self.update_challenge_state('add', 'locked', challenge.pk)
        self.save()

    @property
    def is_mission_completed(self):
        """ consider completed mission if at 
            least one Final Barrier Challenge was completed"""
        return False
        #from web.challenges.models import FinalBarrierChallenge
        #return self.completed.instance_of(FinalBarrierChallenge).exists()

    def unlock_next_block(self):
        """ a barrier has been completed. unlock next block of challenges"""
        log.debug("barrier completed, unlocking next block")
        sorted_challenges = self.mission.challenges_as_sorteddict
        #get index for the barrier (key) of last block
        last_unlocked_barrier_index = max([i for i, x in enumerate(
                                        self.unlocked.instance_of(BarrierChallenge))])
        try:
            next_block = sorted_challenges.value_for_index(last_unlocked_barrier_index+1)
        except IndexError:
            log.error("Mission `%s`: cannot unlock next block.")
            return
        else:

            #TODO there has to be a better way to get the challenge by key index
            def get_last_unlocked_barrier():
                for barrier, challenges in sorted_challenges.items():
                    if challenges == next_block:
                        return barrier
            #if last barrier is a Final Barrier, unlock it
            last_unlocked_barrier = get_last_unlocked_barrier()
            print "last unlocked barrier %s" % last_unlocked_barrier 
            if last_unlocked_barrier.challenge_type == Challenge.FINAL_BARRIER:
                print "unlocking final barrier!"
                self.unlocked.add(last_unlocked_barrier)
                self.locked.remove(last_unlocked_barrier)

            print "unlocking block: %s" % next_block
            # iterate over the challenges and unlock each
            map(lambda ch: self.unlocked.add(ch), next_block)
            map(lambda ch: self.locked.remove(ch), next_block)


    @property
    def this_mission(self):
        return self.this_mission_cached(self.mission.pk)

    @cached(60*60*24*365)
    def this_mission_cached(self, mission_id):
        return self.mission

    def process_completed_challenge(self, challenge_type=None, answer=None):
        # barrier
        if challenge_type == 'barrier':
            # if chosen answer is incorrect, subtract coins
            if answer.selected.is_barrier_correct_answer == False:
                self.coins -= self.this_mission.challenge_coin_value
            self.unlock_next_block()

        # final barrier
        elif challenge_type == 'final_barrier':
            pass

        # regular challenge
        else:
            self.coins += self.this_mission.challenge_coin_value
            # if earned coins for this mission is 3x the challenge_coin_value  
            # then unlock this blocks barrier
            if self.coins <=  self.this_mission.challenge_coin_value  * 3:

                def next_barrier(self):
                    for barrier in Challenge.objects.filter(parent=self.this_mission).\
                            instance_of(BarrierChallenge):
                        if barrier.basetreenode_ptr.get_previous_sibling().get_real_instance() in \
                                self.unlocked.all():
                            return barrier

                next_barrier = next_barrier()
                self.locked.remove(next_barrier)
                self.unlocked.remove(next_barrier)


class UserProfile(models.Model):

    def determine_path(instance, filename):
        return os.path.join('uploads', 'avatars', str(instance.user.id), filename)


    user = models.ForeignKey(User, unique=True)
    instances = models.ManyToManyField(Instance, blank=True, null=True, related_name='user_profiles', through=UserProfilePerInstance)

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

    def __unicode__(self):
        return "%s's profile" % (self.screen_name)

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

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

    instance = kwargs.get('instance')
    if  kwargs.get('created') == True and isinstance(instance, Answer):
        answer = instance
        #print answer
        #print answer.challenge

        challenge = answer.challenge
        mission = challenge.mission
        mst =  mission.mission_states.get(user=answer.user)

        # increment the coins count for non-barrier challenges
        if challenge.challenge_type != Challenge.BARRIER:
            mst.process_completed_challenge()

        # if barrier has been played, unlock next block of challenges
        elif challenge.challenge_type == Challenge.BARRIER:
            mst.process_completed_challenge(challenge_type='barrier', answer=answer)

        # if final barrier has been played, ....
        elif challenge.challenge_type == Challenge.FINAL_BARRIER:
            mst.process_completed_challenge(challenge_type='final_barrier', answer=answer)

        # append to the completed challenges
        #mst.completed.add(challenge)

        mst.save()
post_save.connect(update_player_mission_state, dispatch_uid='update_mission_state')


# Custom hook for adding an anonymous username to the User model.
def user_pre_save(instance, **kwargs):
    if not instance.username:
        instance.username = str(uuid().hex)[:30]

# Custom post save hook for adding group and user profile
def user_post_save(instance, created, **kwargs):
    if created:
        # Create a user profile for the player
        UserProfile.objects.get_or_create(user=instance)
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
