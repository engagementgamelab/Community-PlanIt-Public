import datetime
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

from django.template.defaultfilters import slugify

from gmapsfield.fields import GoogleMapsField
from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^gmapsfield\.fields\.GoogleMapsField"])

#TODO: Make the slug field not null and not blank
#Turn the is_active, is_expired, not started into a view
#Worry about time zone issues, look up how to fix that
#is_notstarted? Sersiouly? How about is_not<insert another noun>
#Fix that and make it part of the view. 
class Instance(models.Model):
    region = models.CharField(max_length=45)
    slug = models.SlugField(null=True, blank=True, editable=False)
    start_date = models.DateField()
    end_date = models.DateField()
    location = GoogleMapsField()
    content = models.TextField(null=True, blank=True)

    curator = models.ForeignKey(User, default=0, null=True, blank=True)

    def is_active(self):
        return self.start_date <= datetime.date.today() and self.end_date >= datetime.date.today()

    def is_expired(self):
        return self.start_date < datetime.date.today() and self.end_date < datetime.date.today()

    def is_notstarted(self):
        return self.start_date > datetime.date.today() and self.end_date > datetime.date.today()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.region)
        super(Instance, self).save()

    def __unicode__(self):
        return self.region[:25]

#TODO: Why is this like this? what possible actions can be taken on an
#instance?
class PointsAssignment(models.Model):
    action = models.CharField(max_length=260)
    points = models.IntegerField(default=0)
    coins = models.IntegerField(default=0)

    instance = models.ForeignKey(Instance, editable=False)

class PointsAssignmentAdmin(admin.ModelAdmin):
    list_display = ('action', 'points', 'coins',)

    def save_model(self, request, obj, form, change):
        obj.instance = request.session.get('admin_instance')
        obj.save()

    def queryset(self, request):
        qs = super(PointsAssignmentAdmin, self).queryset(request)
        return qs.filter(instance=request.session.get('admin_instance'))

class InstanceAdmin(admin.ModelAdmin):
    list_display = ('region', 'start_date', 'end_date',)

#TODO: This just looks broken
def instance_post_save(instance, created, **kwargs):
    if created:
        try:
            actions = ['challenge_completed', 'mapit_completed', 'thinkfast_completed', 'othershoes_completed', 'profile_completed', 'account_created', 'challenge_created', 'comment_created']
            for action in actions:
                p = PointsAssignment(action=action, points=10, instance=instance)
                p.save()
        except: pass

models.signals.post_save.connect(instance_post_save, sender=Instance)


