from uuid import uuid4 as uuid
from django import forms
from web.instances.models import Instance
from web.challenges.models import *
from web.accounts.models import *
from django.contrib import admin
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

def determine_path(instance, filename):
    return 'uploads/'+ str(instance.user.id) +'/'+ filename

class UserProfileIncomes(models.Model):
    income = models.CharField(max_length=128, blank=False, null=False)
    pos = models.IntegerField(blank=False, null=False)
    
    
class UserProfileEducation(models.Model):
    eduLevel = models.CharField(max_length=128)
    pos = models.IntegerField(blank=False, null=False)

class UserProfileLiving(models.Model):
    livingSituation = models.CharField(max_length=128)
    pos = models.IntegerField(blank=False, null=False)

class UserProfile(models.Model):
    accepted_term = models.BooleanField(blank=True)
    accepted_research = models.BooleanField(blank=True)
    phone_number = models.CharField(max_length=12, blank=True, help_text = '<p class="fine">Please use the following phone number format: <em>xxx-xxx-xxx</em>.</p>')
    #Coins is the current number of coins that the player has
    coins = models.IntegerField(default=0)
    #Points is the total points that the player has accrewed
    #TODO: rename this total points, add field for current points,
    # get rid of point multiplier
    points = models.IntegerField(default=0)
    #This is the total number of coins accrewed and this is generally *100
    # Basically TotalPoints - 100*multiplier gives you the number of points to coin
    points_multiplier = models.IntegerField(default=0)
    location_tracking = models.BooleanField(default=False)
    flagged = models.IntegerField(default=0)
    avatar = models.ImageField(upload_to=determine_path, null=True, blank=True)
    affiliations = models.TextField(blank=True, null=True)
    is_of_age = models.BooleanField(default=False)

    # Additional profile fields
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True, blank=True, null=True)
    birth_year = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=64, blank=True, null=True)
    race = models.CharField(max_length=125, blank=True, null=True)
    stake = models.CharField(max_length=125, blank=True, null=True)
    education = models.ForeignKey(UserProfileEducation, blank=True, null=True, default=None)
    income = models.ForeignKey(UserProfileIncomes, blank=True, null=True, default=None)
    living = models.ForeignKey(UserProfileLiving, blank=True, null=True, default=None)

    # Internal fields
    generated_password = models.CharField(max_length=260, editable=False)
    username = models.CharField(max_length=30, unique=True, blank=True, null=True, editable=False)
    completed = models.BooleanField(default=False)
    player_challenges = models.ManyToManyField(PlayerChallenge, blank=True)
    following = models.ManyToManyField(User, related_name='following_user_set', blank=True, null=True)
    user = models.ForeignKey(User, unique=True)
    instance = models.ForeignKey(Instance, blank=True, null=True)

    # comments on the profile from others
    comments = models.ManyToManyField(Comment, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.first_name:
            self.user.first_name = self.first_name

        if self.last_name:
            self.user.last_name = self.last_name

        if self.email:
            self.user.email = self.email

        super(UserProfile, self).save(*args, **kwargs)

    def points_to_coin(self):
        if self.points_multiplier < 1:
            self.points_multiplier = 1
        return 100 - ((self.points_multiplier*100) - self.points)

    def affiliations_csv(self):
        if self.affiliations:
            return self.affiliations.split(", ")

        return ""
    
    def points_progress(self):
        return self.points % 100

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __unicode__(self):
        return self.user.email[:25] +"'s Profile"

    def screen_name(self):
        first = self.first_name or self.user.first_name or ''
        last = self.last_name or self.user.last_name or ''
        last = len(last) > 1 and last[0].upper() + '.' or last

        if first or last:
            return "%s%s" % (first, last and ' ' + last or '')

        return 'Anonymous'

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
    anon = str(uuid().hex)[:30]

    if not instance.username:
        instance.username = anon

# Custom post save hook for adding group and user profile
def user_post_save(instance, created, **kwargs):
    if created:
        # Create a user profile for the player and add them to the
        # `Player` group.  Default the player to inactive.
        try:
            UserProfile.objects.create(user=instance)
            instance.groups.add(Group.objects.get(name='Player'))
            instance.is_active = False
        
        # If the Player group is deleted, recreate it.
        except Group.DoesNotExist:
            group = Group(name='Player')
            group.save()
            instance.groups.add(group)

models.signals.pre_save.connect(user_pre_save, sender=User)
models.signals.post_save.connect(user_post_save, sender=User)
