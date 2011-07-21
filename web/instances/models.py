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
class Instance(models.Model):
    name = models.CharField(max_length=45)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2)
    slug = models.SlugField(editable=False)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True, default=None)
    location = GoogleMapsField()
    content = models.TextField(null=True, blank=True)
    process_name = models.CharField(max_length=255, null=True, blank=True)
    process_description = models.TextField(null=True, blank=True)
    curators = models.ManyToManyField(User)
    
    #This should go into a view, djagno doesn't support views... this is
    # a terrible thing and honestly, there are so many problems associated
    # with trying to plug this into a view, that it's just simpler to do this
    # bad bad, terrbile code - BMH
    def is_active(self):
        if datetime.datetime.now() >= self.start_date and datetime.datetime.now() <= self.end_date:
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
        
    def __unicode__(self):
        return self.name[:25]

#TODO: Perhaps this should be in it's own project
class PointsAssignment(models.Model):
    action = models.CharField(max_length=260)
    points = models.IntegerField(default=0)
    coins = models.IntegerField(default=0)

    instance = models.ForeignKey(Instance, editable=False)

class InstanceAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date',)


