import datetime
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

from django.template.defaultfilters import slugify

from gmapsfield.fields import GoogleMapsField
from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^gmapsfield\.fields\.GoogleMapsField"])

#TODO: Worry about time zone issues, look up how to fix that if it needs to be
#Also test this.

#This is the physical data. All FKs are made off of this, but all data
#can be used through Instance. Look in the instances/management/__init__.py
#to see the view that is created 
class InstanceView(models.Model):
    name = models.CharField(max_length=45)
    slug = models.SlugField()
    start_date = models.DateField()
    end_date = models.DateField()
    location = GoogleMapsField()
    content = models.TextField(null=True, blank=True)
    curator = models.ForeignKey(User, default=0, null=True, blank=True)
    
#This is a view
class Instance(InstanceView):
    is_active = models.BooleanField(editable=False)
    is_expired = models.BooleanField(editable=False)
    is_started = models.BooleanField(editable=False)
    
    class Meta: 
        managed = False
        
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Instance,self).save()
        
    def __unicode__(self):
        return self.name[:25]

#TODO: Perhaps this should be in it's own project
class PointsAssignment(models.Model):
    action = models.CharField(max_length=260)
    points = models.IntegerField(default=0)
    coins = models.IntegerField(default=0)

    instance = models.ForeignKey(InstanceView, editable=False)

class PointsAssignmentAdmin(admin.ModelAdmin):
    list_display = ('action', 'points', 'coins',)

    def save_model(self, request, obj, form, change):
        obj.instance = request.session.get('admin_instance')
        obj.save()

    def queryset(self, request):
        qs = super(PointsAssignmentAdmin, self).queryset(request)
        return qs.filter(instance=request.session.get('admin_instance'))

class InstanceAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date',)

#TODO: Make sure that this is unit tested upon instance creation! DO IT!
def instance_post_save(instance, created, **kwargs):
    if (PointsAssignment.objects.filter(instance=instance).count() == 0):
        f = open("/home/ben/djangoOut", "w")
        f.write("InstanceID: %s created: %s" % (instance.id, created))
        actions = ['challenge_completed', 'mapit_completed', 'thinkfast_completed', 'othershoes_completed', 'profile_completed', 'account_created', 'challenge_created', 'comment_created']
        for action in actions:
            p = PointsAssignment(action=action, points=10, instance=instance)
            p.save()

models.signals.post_save.connect(instance_post_save, sender=Instance)

