__all__ = (
    'Language', 'Instance', 'PointsAssignment', 'NotificationRequest', 'Affiliation',
)

import os.path
import datetime

from stream import utils as stream_utils
from cache_utils.decorators import cached

from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
from django.utils.safestring import mark_safe
from django.utils.translation import get_language
from django.core.urlresolvers import reverse

from django.contrib import admin
from django.contrib.auth.models import User

from dateutil.relativedelta import relativedelta
from gmapsfield.fields import GoogleMapsField
from nani.models import TranslatableModel, TranslatedFields
from nani.manager import TranslationManager
from south.modelsinspector import add_introspection_rules

import logging
log = logging.getLogger(__name__)

add_introspection_rules([], ["^gmapsfield\.fields\.GoogleMapsField"])

def determine_path(instance, filename):
    return os.path.join('uploads/cities/', str(instance.domain), filename)


class Language(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('code',)


class Affiliation(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, blank=True, default='')

    def __unicode__(self):
        return "%s" %(self.name,)

    def save(self, *args, **kwargs):
        if self.slug is None or self.slug == '':
            self.slug = slugify(self.name)[:100]
        super(Affiliation, self).save()

    @models.permalink
    def get_absolute_url(self):
        return ('affiliations:affiliation', (self.slug, ))

    class Meta:
        ordering = ('name',)



class InstanceManager(TranslationManager):

    def __init__(self, *args, **kwargs):
        super(InstanceManager, self).__init__(*args, **kwargs)
        self.now = datetime.datetime.now()


    @cached(60*60*24*7)
    def for_slug(self, slug):
        return self.get(slug=slug)

    def common_excludes(self):
        return self.exclude(is_disabled=True)

    def future(self):
        qs = self.language(get_language()).exclude(is_disabled=True)
        return qs.filter(start_date__gt=self.now).distinct()

    def present(self):
        qs = self.language(get_language()).exclude(is_disabled=True)
        return qs.filter(start_date__lte=self.now, missions__end_date__gte=self.now).language(get_language()).distinct()

    def past(self):
        qs = self.language(get_language()).exclude(is_disabled=True)
        return qs.exclude(missions__end_date__gte=self.now).distinct()

    @cached(60*60*24)
    def current(self):
        # basically, active and future
        qs = self.language(get_language()).exclude(is_disabled=True)
        return qs.filter(missions__end_date__gte=self.now).distinct()

    def latest_for_city_domain(self, domain):
        #looks like `latest` qs method is broken in django-nani
        #applying a workaround for now.
        #TODO fix
        from core.utils import _fake_latest
        kwargs = dict(
                for_city__domain=domain,
                start_date__lte=self.now,
                missions__end_date__gte=self.now,
        )
        qs = self.filter(**kwargs)
        return _fake_latest(Instance, qs)


class Instance(TranslatableModel):

    (BOSTON, DETROIT, PHILADELPHIA, NYC) = xrange(4)
    INSTANCE_CITIES = (
            (BOSTON, 'Boston'),
            (DETROIT, 'Detroit'),
            (PHILADELPHIA, 'Philadelphia'),
            (NYC, 'New York City'),
    )

    slug = models.SlugField()
    title = models.CharField(max_length=255, verbose_name="Title (non-translatable)")
    state = models.CharField(max_length=2)
    start_date = models.DateTimeField()
    location = GoogleMapsField()
    curators = models.ManyToManyField(User, blank=True)
    languages = models.ManyToManyField(Language)
    days_for_mission = models.IntegerField(default=7)
    city = models.IntegerField(max_length=2, choices=INSTANCE_CITIES, null=True)


    translations = TranslatedFields(
        description = models.TextField(),
        #meta = {'get_latest_by': 'start_date'}
    )

    # prevent the game from being visible on the site
    is_disabled = models.BooleanField(default=False, verbose_name="Disable the game from being visible on the site")

    objects = InstanceManager()

    class Meta:
        get_latest_by = 'start_date'
        ordering = ('start_date',)

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('instances:instance', (), {
            'slug': self.slug,
        })

    @property
    def default_language(self):
        return Language.objects.get(code=settings.LANGUAGE_CODE)

    @property
    def stream_action_title(self):
        return self.title

    def coin_count(self):
        return self.user_profiles.aggregate(models.Sum('currentCoins')).get('currentCoins', 0)

    #def dump_users(self):
    #    from accounts.models import UserProfile
    #    profiles = UserProfile.objects.filter(instance=self)
    #    out = ["Instance: %s" % self.title,]
    #    for prof in profiles:
    #        u = prof.user
    #        prefix = u""
    #        if u in self.curators.all():
    #            prefix = u"CURATOR: "
    #        out.append(u"%s %s %s <%s>, username: %s" %(prefix, u.first_name.capitalize(), u.last_name.capitalize(), 
    #                                            prof.email, u.username)
    #        )
    #    return out
    
    @property
    def end_date(self):
        missions = self.missions.order_by('-end_date')
        if missions:
            last_mission = missions[0]
            return last_mission.end_date
        return None
    
    @property 
    def is_future(self):
        ''' Instance is not yet running (pre-game)'''
        return self in Instance.objects.future()
        
    @property 
    def is_present(self):
        ''' Instance is currently running (during-game) '''
        return self in Instance.objects.present()

    @property 
    def is_past(self):
        ''' Instance is finished running (post-game)'''
        return self in Instance.objects.past()

    @property
    def is_started(self):
        ''' Active and Expired Games '''
        return datetime.datetime.now() >= self.start_date
    
    def time_until_start(self):
        return self.start_date - datetime.datetime.now()
    
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

    def get_slideshow_attachment(self):
        attachments = self.attachment_set.all()
        return attachments.filter(is_slideshow=True)[0] if attachments.filter(is_slideshow=True) else None
        
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

