import datetime

from django.db import models
from django.db.models import Q
from django.template.defaultfilters import slugify
from django.utils.safestring import mark_safe

from django.contrib import admin
from django.contrib.auth.models import User

from dateutil.relativedelta import relativedelta
from gmapsfield.fields import GoogleMapsField
from nani.models import TranslatableModel, TranslatedFields
from nani.manager import TranslationManager
from nani.utils import get_translation_aware_manager
from south.modelsinspector import add_introspection_rules

add_introspection_rules([], ["^gmapsfield\.fields\.GoogleMapsField"])

__all__ = (
    'Language', 'Instance', 'PointsAssignment', 'NotificationRequest',
)


class Language(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return "%s <%s>" %(self.name, self.code)

class InstanceManager(TranslationManager):

    def past(self):
        now = datetime.datetime.now()
        return self.filter(missions__end_date__lt=now).order_by('start_date')

    def future(self):
        return self.filter(start_date__gt=datetime.datetime.now()).order_by('start_date')

    def active(self):
        now = datetime.datetime.now()
        return self.filter(start_date__lte=now, missions__end_date__gte=now).order_by('start_date').distinct()

class Instance(TranslatableModel):
    slug = models.SlugField()
    title = models.CharField(max_length=255, verbose_name="Title (non-translatable)")
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2)
    start_date = models.DateTimeField()
    location = GoogleMapsField()
    curators = models.ManyToManyField(User)
    languages = models.ManyToManyField(Language)
    days_for_mission = models.IntegerField(default=7)

    translations = TranslatedFields(
        description = models.TextField(),
        #meta = {'get_latest_by': 'start_date'}
    )
    objects = InstanceManager()

    class Meta:
        get_latest_by = 'start_date'
        
    def __unicode__(self):
        return self.title

    def coin_count(self):
        return self.user_profiles.aggregate(models.Sum('currentCoins')).get('currentCoins', 0)

    def dump_users(self):
        from accounts.models import UserProfile
        profiles = UserProfile.objects.filter(instance=self)
        out = ["Instance: %s" % self.title,]
        for prof in profiles:
            u = prof.user
            prefix = u""
            if u in self.curators.all():
                prefix = u"CURATOR: "
            out.append(u"%s %s %s <%s>, username: %s" %(prefix, u.first_name.capitalize(), u.last_name.capitalize(), 
                                                u.email, u.username)
            )
        return out
        
    def end_date(self):
        missions = self.missions.order_by('-end_date')
        if missions:
            last_mission = missions[0]
            return last_mission.end_date
        return None
    
    def is_active(self):
        return self in Instance.objects.active()

    def is_expired(self):
        return self in Instance.objects.past()
    
    def is_started(self):
        return datetime.datetime.now() >= self.start_date

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)[:50]
        super(Instance,self).save()
        
class Stake(TranslatableModel):
    """
    The stakes users hold in the community, e.g. Live, Work, Play, or Teacher,
    Administrator, Student.
    """
    instance = models.ForeignKey(Instance, related_name='stakes')
    pos = models.IntegerField(blank=False, null=False)

    translations = TranslatedFields(
        stake = models.CharField(max_length=128),
    )

    class Meta:
        ordering = ('instance', 'pos')

    def __unicode__(self):
        return self.stake

#TODO: Perhaps this should be in it's own project
class PointsAssignment(models.Model):
    action = models.CharField(max_length=260)
    points = models.IntegerField(default=0)
    coins = models.IntegerField(default=0)

    instance = models.ForeignKey(Instance, editable=False)

class NotificationRequest(models.Model):
    instance = models.ForeignKey(Instance, related_name='notification_requests')
    email = models.EmailField()

    class Meta:
        unique_together = ['instance', 'email']

    def __unicode__(self):
        return '{0}: {1}'.format(self.instance, self.email)
