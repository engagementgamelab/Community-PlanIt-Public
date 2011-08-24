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

from web.accounts.models import *
from web.challenges.models import *
from web.instances.models import Instance

def determine_path(instance, filename):
    return 'uploads/'+ str(instance.user.id) +'/'+ filename

class UserProfileIncomes(models.Model):
    income = models.CharField(max_length=128)
    pos = models.IntegerField(blank=False, null=False)

    def __unicode__(self):
        return self.income
    
class UserProfileEducation(models.Model):
    eduLevel = models.CharField(max_length=128)
    pos = models.IntegerField(blank=False, null=False)

    def __unicode__(self):
        return self.eduLevel

class UserProfileLiving(models.Model):
    livingSituation = models.CharField(max_length=128)
    pos = models.IntegerField(blank=False, null=False)

    def __unicode__(self):
        return self.livingSituation

class UserProfileGender(models.Model):
    gender = models.CharField(max_length=128)
    pos = models.IntegerField(blank=False, null=False)

    def __unicode__(self):
        return self.gender

class UserProfileRace(models.Model):
    race = models.CharField(max_length=128)
    pos = models.IntegerField(blank=False, null=False)

    def __unicode__(self):
        return self.race

class UserProfileStake(models.Model):
    stake = models.CharField(max_length=128)
    pos = models.IntegerField(blank=False, null=False)

    def __unicode__(self):
        return self.stake
    
class UserProfile(models.Model):
    #Foreign key fields
    user = models.ForeignKey(User, unique=True)
    instance = models.ForeignKey(Instance, blank=True, null=True, related_name='user_profiles')
    gender = models.ForeignKey(UserProfileGender, blank=True, null=True, default=None)
    race = models.ForeignKey(UserProfileRace, blank=True, null=True, default=None)
    stake = models.ForeignKey(UserProfileStake, blank=True, null=True, default=None)
    education = models.ForeignKey(UserProfileEducation, blank=True, null=True, default=None)
    income = models.ForeignKey(UserProfileIncomes, blank=True, null=True, default=None)
    living = models.ForeignKey(UserProfileLiving, blank=True, null=True, default=None)
    
    accepted_term = models.BooleanField(default=False)
    accepted_research = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=12, blank=True, help_text = '<p class="fine">Please use the following phone number format: <em>xxx-xxx-xxx</em>.</p>')
    # the current number of coins that the player has
    currentCoins = models.IntegerField(default=0)
    # the total points that the player has accrued
    totalPoints = models.IntegerField(default=0)
    # points to the next coin
    coinPoints = models.IntegerField(default=0)
        
    flagged = models.BooleanField(default=0)
    avatar = models.ImageField(upload_to=determine_path, null=True, blank=True)
    affiliations = models.TextField(blank=True, null=True)
    editedProfile = models.BooleanField(default=0)
    receive_email = models.BooleanField(default=True)
    # Additional profile fields
    birth_year = models.IntegerField(blank=True, null=True)

    # Internal fields
    following = models.ManyToManyField(User, related_name='following_user_set', blank=True, null=True)

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

class UserProfileInline(admin.StackedInline):
    model = UserProfile

class UserCreationForm(UserCreationForm):
    username = forms.CharField(label="Username", initial=str(uuid().hex)[:30])

class UserChangeForm(UserChangeForm):
    username = forms.CharField(label="Username")

class UserProfileAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    
    inlines = [ UserProfileInline, ]
    list_display = ('email', 'first_name', 'last_name',)
    obj = None
    always_show_username = False

    def get_form(self, request, obj=None, **kwargs):
        self.obj = obj 
        return super(UserProfileAdmin, self).get_form(request, obj, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'player_challenges' and getattr(self, 'obj', None):
            kwargs['queryset'] = UserProfile.objects.get(id=self.obj.id).player_challenges.all()
        elif db_field.name == 'player_challenges':
            kwargs['queryset'] = UserProfile.objects.filter(id=-2)

        if db_field.name == 'following' and getattr(self, 'obj', None):
            kwargs['queryset'] = UserProfile.objects.get(id=self.obj.id).following.all()
        elif db_field.name == 'following':
            kwargs['queryset'] = UserProfile.objects.filter(id=-2)

        if db_field.rel.to == User:
            field.label_from_instance = self.get_user_label

        return super(UserProfileAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super(UserProfileAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

        if db_field.rel.to == User:
            field.label_from_instance = self.get_user_label

        return field

    def get_user_label(self, user):
        name = user.get_full_name()
        return name
        username = user.username
        if not self.always_show_username:
            return name or username
        return (name and name != username and '%s (%s)' % (name, username)
                or username)

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

        UserProfile.objects.create(user=instance)
        instance.is_active = False
        instance.groups.add(player_group)

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
