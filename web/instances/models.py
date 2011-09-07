import datetime

from django.db import models
from django.db.models import Q
from django.template.defaultfilters import slugify
from django.utils.safestring import mark_safe

from django.contrib import admin
from django.contrib.auth.models import User

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
        # TODO deal with instance end dates
        #return self.filter(end_date__lt=datetime.now()).order_by('start_date')
        return self.filter()

    def future(self):
        return self.filter(start_date__gt=datetime.datetime.now()).order_by('start_date')

    def active(self):
        # TODO deal with instance end dates
        #now = datetime.now()
        #return self.filter(start_date__lte=now).filter(Q(end_date__isnull=True)|Q(end_date__gte=now)).order_by('start_date')
        return self.filter()


class Instance(TranslatableModel):
    slug = models.SlugField(editable=False) #unique can not be enforced here, editing throws a unique constraint error
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
        

    #def end_date(self):
    #    mgr = get_translation_aware_manager(Mission)
    #    mgr.filter()
    
    #TODO 
    # rewrite this using the last mission end date as the end date
    def is_active(self):
        now = datetime.datetime.now()
        if now >= self.start_date: #and (self.end_date is None or now <= self.end_date):
            return True;
        else:
            return False;

    #TODO 
    # rewrite this using the last mission end date as the end date
    def is_expired(self):
        #if self.end_date and datetime.now() >= self.end_date:
        #    return True
        #else:
        #    return False
        return False
    
    def is_started(self):
        return datetime.datetime.now() >= self.start_date

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
        
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)[:50]
        super(Instance,self).save()
        
    def __unicode__(self):
        return self.title

    def coin_count(self):
        return self.user_profiles.aggregate(models.Sum('currentCoins')).get('currentCoins', 0)

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
