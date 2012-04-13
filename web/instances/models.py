import os.path
import datetime

from stream import utils as stream_utils
#from cache_utils.decorators import cached

from django.db import models
from django.template.defaultfilters import slugify
from django.utils.safestring import mark_safe

from django.contrib import admin
from django.contrib.auth.models import User

from dateutil.relativedelta import relativedelta
from gmapsfield.fields import GoogleMapsField
from nani.models import TranslatableModel, TranslatedFields
from nani.manager import TranslationManager
from south.modelsinspector import add_introspection_rules

add_introspection_rules([], ["^gmapsfield\.fields\.GoogleMapsField"])

__all__ = (
    'City', 'Language', 'Instance', 'PointsAssignment', 'NotificationRequest', 'Affiliation',
)

def determine_path(instance, filename):
    return os.path.join('uploads/cities/', str(instance.domain), filename)

class CityManager(models.Manager):
	pass

    #def city_by_domain(self):
    #    return City.objects.

class City(models.Model):
    name = models.CharField(max_length=100)
    domain = models.CharField(max_length=100)
    description = models.TextField(null=False, blank=True, default='')
    image = models.ImageField(upload_to=determine_path, null=True, blank=True)

    objects = CityManager()

    def __unicode__(self):
        return "%s at <%s>" %(self.name, self.domain)

    class Meta:
        verbose_name_plural = 'Cities'


class Language(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return "%s <%s>" %(self.name, self.code)


class Affiliation(models.Model):
    slug = models.SlugField()
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, blank=True, default='')

    def __unicode__(self):
        return "%s" %(self.name,)

    def save(self, *args, **kwargs):
        if not self.slug or self.slug == '':
            self.slug = slugify(self.name)[:100]
        super(Affiliation, self).save()


class InstanceManager(TranslationManager):

    def past(self):
        now = datetime.datetime.now()
        return self.exclude(missions__end_date__gte=now).order_by('start_date')

    def future(self):
        return self.filter(start_date__gt=datetime.datetime.now()).order_by('start_date')

    def active(self):
        now = datetime.datetime.now()
        return self.filter(start_date__lte=now, missions__end_date__gte=now).order_by('start_date').distinct()
    
    def current(self):
        # basically, active and future 
        now = datetime.datetime.now()
        return self.filter(missions__end_date__gte=now).order_by('start_date').distinct()
        
    #@cached(60*60*24, 'instances')
    def for_city(self, domain):
        return self.filter(for_city__domain=domain)
    
    def past_for_city(self, domain):
        now = datetime.datetime.now()
        return self.filter(for_city__domain=domain).exclude(missions__end_date__gte=now).order_by('start_date')
        
    def future_for_city(self, domain):
        return self.filter(for_city__domain=domain).filter(start_date__gt=datetime.datetime.now()).order_by('start_date')

    def active_for_city(self, domain):
        now = datetime.datetime.now()
        return self.filter(for_city__domain=domain).filter(start_date__lte=now, missions__end_date__gte=now).order_by('start_date').distinct()

    def current_for_city(self, domain):
        now = datetime.datetime.now()
        return self.filter(for_city__domain=domain).filter(missions__end_date__gte=now).order_by('start_date').distinct()
        

    def latest_for_city_domain(self, domain):
        #looks like `latest` qs method is broken in django-nani
        #applying a workaround for now.
        #TODO fix
        from core.utils import _fake_latest
        now = datetime.datetime.now()
        kwargs = dict(
                for_city__domain=domain,
                start_date__lte=now,
                missions__end_date__gte=now,
        )
        qs = self.filter(**kwargs)
        return _fake_latest(Instance, qs)


class Instance(TranslatableModel):
    slug = models.SlugField()
    title = models.CharField(max_length=255, verbose_name="Title (non-translatable)")
    state = models.CharField(max_length=2)
    start_date = models.DateTimeField()
    location = GoogleMapsField()
    curators = models.ManyToManyField(User)
    languages = models.ManyToManyField(Language)
    days_for_mission = models.IntegerField(default=7)
    for_city = models.ForeignKey(City, null=True, related_name='instances')

    translations = TranslatedFields(
        description = models.TextField(),
        #meta = {'get_latest_by': 'start_date'}
    )
    objects = InstanceManager()

    class Meta:
        get_latest_by = 'start_date'
        
    def __unicode__(self):
        return self.title

    def get_absolute_url(self, ssl=True):
        if ssl == True:
            return "".join(['https://', self.for_city.domain])
        return "".join(['http://', self.for_city.domain])

    @property
    def stream_action_title(self):
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
                                                prof.email, u.username)
            )
        return out
        
    def end_date(self):
        missions = self.missions.order_by('-end_date')
        if missions:
            last_mission = missions[0]
            return last_mission.end_date
        return None
    
    def time_until_start(self):
        return self.start_date - datetime.datetime.now()
    
    def is_active(self):
        return self in Instance.objects.active()

    def is_expired(self):
        return self in Instance.objects.past()
    
    def is_started(self):
        return datetime.datetime.now() >= self.start_date

    def rebuild_mission_dates(self):
        # this will reset all start_date, end_date fields on 
        # this instances missions

        def _reset_fields(m, starton=None):
            if not starton:
                starton = m.instance.start_date
            m.start_date = starton
            m.end_date = m.start_date + relativedelta(days=+m.instance.days_for_mission, hour=23, minute=59, second=59)
            m.save()
            return m.end_date

        starton = None
        for m in  self.missions.all().distinct().order_by('date_created'):
            starton = _reset_fields(m, starton) + relativedelta(seconds=+1)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)[:50]
        super(Instance,self).save()
        if self.start_date:
            self.rebuild_mission_dates()

stream_utils.register_target(Instance)

class PointsAssignmentAction(models.Model):
    action = models.CharField(max_length=260)

    class Meta:
        ordering = ('action',)

    def __unicode__(self):
        return self.action[:50]

class PointsAssignment(models.Model):
    action = models.ForeignKey(PointsAssignmentAction, related_name='points_assignments')
    points = models.IntegerField(default=0)

    instance = models.ForeignKey(Instance, related_name='points_assignments')

    class Meta:
        ordering = ('action__action', 'instance', 'points')

    def __unicode__(self):
        return '%d: %s' % (self.points, self.action)

class NotificationRequest(models.Model):
    instance = models.ForeignKey(Instance, related_name='notification_requests')
    email = models.EmailField()

    class Meta:
        unique_together = ['instance', 'email']

    def __unicode__(self):
        return '{0}: {1}'.format(self.instance, self.email)
