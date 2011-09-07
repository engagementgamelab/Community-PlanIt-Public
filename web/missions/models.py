import datetime
from dateutil.relativedelta import relativedelta
from django.template.defaultfilters import slugify
from django.db import models
from django.contrib import admin

from nani.admin import TranslatableAdmin
from nani.models import TranslatableModel, TranslatedFields
from nani.manager import TranslationManager

from instances.models import Instance

def rebuild_mission_dates(instance=None):
    # this will reset all start_date, end_date fields
    # will conflict with Mission.save()
    # you have been warned

    def _reset_fields(m, starton=None):
        if not starton:
            starton = m.instance.start_date
        m.start_date = starton
        m.end_date = m.start_date + relativedelta(days=+m.instance.days_for_mission)
        m.save()
        return m.end_date

    for instance in Instance.objects.untranslated():
        starton = None
        for m in  Mission.objects.filter(instance=instance).order_by('date_created'):
            starton = _reset_fields(m, starton)


class MissionManager(TranslationManager):

    def latest_by_instance(self, instance):
        missions_for_instance = self.filter(instance=instance)
        if missions_for_instance:
            latest_by =  max(missions_for_instance.values_list('end_date', flat=True))
            return self.get(**dict(end_date=latest_by))

        return self.none()

    def past(self, instance=None):
        kwargs = dict(end_date__lt=datetime.datetime.now(),)
        if instance:
            kwargs.update(dict(instance=instance))
        return self.filter(**kwargs).order_by('-end_date')

    def future(self, instance=None):
        kwargs = dict(start_date__gt=datetime.datetime.now(),)
        if instance:
            kwargs.update(dict(instance=instance))
        return self.filter(**kwargs).order_by('start_date')

    def active(self, instance=None):
        now = datetime.datetime.now()
        kwargs = dict(start_date__lte=now, end_date__gte=now,)
        if instance:
            kwargs.update(dict(instance=instance))
        return self.filter(**kwargs).order_by('start_date')


class Mission(TranslatableModel):

    title = models.CharField(max_length=255, verbose_name="Title (non-translatable)")
    instance = models.ForeignKey(Instance, related_name='missions')
    slug = models.SlugField(editable=False)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    video = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    translations = TranslatedFields(
        name = models.CharField(max_length=255, blank=True),
        description = models.TextField(blank=True),
        #meta = {'get_latest_by': 'start_date'}
    )

    objects = MissionManager()

    class Meta:
        pass
        #get_latest_by = 'start_date'

    def is_active(self):
        now = datetime.datetime.now()
        return self.start_date <= now and now <= self.end_date
        
    def is_expired(self):
        return datetime.datetime.now() > self.end_date
    
    def is_started(self):
        return datetime.datetime.now() >= self.start_date

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)[:50]
        if not self.start_date and not self.end_date:
            try:
                latest = Mission.objects.latest_by_instance(self.instance)
            except ValueError:
                self.start_date = datetime.now()
                self.end_date = self.start_date + relativedelta(days=+self.instance.days_for_mission)
            else:
                self.start_date = latest.end_date
                self.end_date = latest.end_date + relativedelta(days=+self.instance.days_for_mission)
        super(Mission, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

class MissionAdmin(TranslatableAdmin):
    list_display = ('title', 'instance', 'start_date', 'end_date')
