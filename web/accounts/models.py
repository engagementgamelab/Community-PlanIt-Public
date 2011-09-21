import datetime
from uuid import uuid4 as uuid

from django import forms
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

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
from web.instances.models import Instance

def determine_path(instance, filename):
    return 'uploads/'+ str(instance.user.id) +'/'+ filename

class UserProfileOptionBase(TranslatableModel):
    pos = models.IntegerField(blank=False, null=False)
    instance = models.ForeignKey(Instance)

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


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    instance = models.ForeignKey(Instance, blank=True, null=True, related_name='user_profiles')

    avatar = models.ImageField(upload_to=determine_path, null=True, blank=True)
    email = models.EmailField(_('e-mail address'), blank=True, max_length=250)
    receive_email = models.BooleanField(default=True)
    city = models.CharField(max_length=128, blank=True, default='')
    zip_code = models.CharField(max_length=10, blank=True, default='')
    stake = models.ForeignKey(UserProfileStake, blank=True, null=True, default=None)
    preferred_language = models.CharField(max_length=5, default='en-us')
    affiliations = models.TextField(blank=True, null=True, default='')

    # Additional profile fields
    birth_year = models.IntegerField(blank=True, null=True, default=0)
    gender = models.ForeignKey(UserProfileGender, blank=True, null=True, default=None)
    race = models.ForeignKey(UserProfileRace, blank=True, null=True, default=None)
    education = models.ForeignKey(UserProfileEducation, blank=True, null=True, default=None)
    income = models.ForeignKey(UserProfileIncome, blank=True, null=True, default=None)
    living = models.ForeignKey(UserProfileLivingSituation, blank=True, null=True, default=None)
    how_discovered = models.ForeignKey(UserProfileHowDiscovered, blank=True, null=True, default=None)
    how_discovered_other = models.CharField(max_length=128, blank=True, default='')

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
        return self.screen_name +"'s profile"

    def affiliations_csv(self):
        if self.affiliations:
            return self.affiliations.split(", ")

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
        return reverse(
            'generic_redirect',
            args=(self.content_type_id, self.object_id)
        )
