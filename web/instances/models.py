import os.path
import datetime

from stream import utils as stream_utils
from cache_utils.decorators import cached
from polymorphic_tree.models import PolymorphicMPTTModel, PolymorphicTreeForeignKey
from polymorphic_tree.managers import PolymorphicMPTTModelManager
#from polymorphic import PolymorphicManager
from dateutil.relativedelta import relativedelta
from gmapsfield.fields import GoogleMapsField
from south.modelsinspector import add_introspection_rules

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext as _
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

import logging
log = logging.getLogger(__name__)

add_introspection_rules([], ["^gmapsfield\.fields\.GoogleMapsField"])


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


class InstanceManager(PolymorphicMPTTModelManager):

    @cached(60*60*24*7)
    def for_slug(self, slug):
        return self.get(slug=slug)

    def common_excludes(self):
        return self.exclude(is_disabled=True)

    def future(self):
        qs = self.exclude(is_disabled=True)
        return qs.filter(start_date__gt=self.now).distinct()

    def present(self):
        qs = self.exclude(is_disabled=True)
        return qs.filter(start_date__lte=self.now, missions__end_date__gte=self.now).distinct()

    def past(self):
        qs = self.exclude(is_disabled=True)
        return qs.exclude(missions__end_date__gte=self.now).distinct()

    @cached(60*60*24)
    def current(self):
        # basically, active and future
        qs = self.exclude(is_disabled=True)
        return qs.filter(missions__end_date__gte=self.now).distinct()

# A base model for the tree:

class BaseTreeNode(PolymorphicMPTTModel):
    parent = PolymorphicTreeForeignKey('self', blank=True, null=True, related_name='children', verbose_name=_('parent'))
    title = models.CharField(_("Title"), max_length=200)

    inst = InstanceManager()

    class Meta:
        verbose_name = _("Tree node")
        verbose_name_plural = _("Tree nodes")



class Instance(BaseTreeNode):

    (BOSTON, DETROIT, PHILADELPHIA, NYC) = xrange(4)
    INSTANCE_CITIES = (
            (BOSTON, 'Boston'),
            (DETROIT, 'Detroit'),
            (PHILADELPHIA, 'Philadelphia'),
            (NYC, 'New York City'),
    )
    slug = models.SlugField()
    state = models.CharField(max_length=2)
    start_date = models.DateTimeField()
    location = GoogleMapsField(blank=True)
    curators = models.ManyToManyField(User, blank=True)
    days_for_mission = models.IntegerField(default=7)
    city = models.IntegerField(max_length=2, choices=INSTANCE_CITIES, null=True)
    description = models.TextField()

    # prevent the game from being visible on the site
    is_disabled = models.BooleanField(default=False, verbose_name="Disable the game from being visible on the site")


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
    def stream_action_title(self):
        return self.title

    def coin_count(self):
        return self.user_profiles.aggregate(models.Sum('currentCoins')).get('currentCoins', 0)

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

    def get_slideshow_attachment(self):
        attachments = self.attachment_set.all()
        return attachments.filter(is_slideshow=True)[0] if attachments.filter(is_slideshow=True) else None

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.title)[:50]
        super(Instance, self).save()

stream_utils.register_target(Instance)
