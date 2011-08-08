import datetime

from django.db import models
from django.template.defaultfilters import slugify
from django.utils.safestring import mark_safe

from django.contrib import admin
from django.contrib.auth.models import User

from gmapsfield.fields import GoogleMapsField
from south.modelsinspector import add_introspection_rules

add_introspection_rules([], ["^gmapsfield\.fields\.GoogleMapsField"])

class InstanceQueryMixin(object):
    def past(self):
        return self.filter(end_date__lt=datetime.datetime.now()).order_by('start_date')

    def future(self):
        return self.filter(start_date__gt=datetime.datetime.now()).order_by('start_date')

    def active(self):
        now = datetime.datetime.now()
        return self.filter(start_date__lte=now).filter(end_date__gte=now).order_by('start_date')

class InstanceQuerySet(models.query.QuerySet, InstanceQueryMixin):
    pass

class InstanceManager(models.Manager, InstanceQueryMixin):
    def get_query_set(self):
        return InstanceQuerySet(self.model, using=self._db)

class Instance(models.Model):
    name = models.CharField(max_length=45)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2)
    slug = models.SlugField(unique=True, editable=False)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True, default=None)
    location = GoogleMapsField()
    content = models.TextField(null=True, blank=True)
    process_name = models.CharField(max_length=255, null=True, blank=True)
    process_description = models.TextField(null=True, blank=True)
    curators = models.ManyToManyField(User)

    objects = InstanceManager()

    class Meta:
        get_latest_by = 'start_date'
        
    def __unicode__(self):
        return self.name
    
    def is_active(self):
        now = datetime.datetime.now()
        if now >= self.start_date and now <= self.end_date:
            return True;
        else:
            return False;
        
    def is_expired(self):
        if datetime.datetime.now() >= self.end_date:
            return True
        else:
            return False
    
    def is_started(self):
        if datetime.datetime.now() >= self.start_date:
            return True
        else:
            return False
        
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Instance,self).save()

    def coin_count(self):
        return self.user_profiles.aggregate(models.Sum('currentCoins')).get('currentCoins', 0)

#TODO: Perhaps this should be in it's own project
class PointsAssignment(models.Model):
    action = models.CharField(max_length=260)
    points = models.IntegerField(default=0)
    coins = models.IntegerField(default=0)

    instance = models.ForeignKey(Instance, editable=False)

class InstanceAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date',)

class NotificationRequest(models.Model):
    instance = models.ForeignKey(Instance, related_name='notification_requests')
    email = models.EmailField()

    class Meta:
        unique_together = ['instance', 'email']

    def __unicode__(self):
        return '{0}: {1}'.format(self.instance, self.email)
