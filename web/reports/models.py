from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from web.instances.models import Instance
from gmapsfield.fields import GoogleMapsField

class Activity(models.Model):
    action = models.CharField(max_length=48)
    data = models.TextField()
    url = models.URLField(blank=True, null=True)
    location = GoogleMapsField(blank=True, null=True) # Make editable false
    date = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=255)

    user = models.ForeignKey(User, blank=True, null=True)
    instance = models.ForeignKey(Instance, blank=True, null=True, editable=False)
    
    class Meta:
        verbose_name = 'Activity'
        verbose_name_plural = 'Activities'

    def __unicode__(self):
        label = self.action +' - '+ self.data
        return label

class ActivityAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.instance = request.session.get('admin_instance')
        obj.save()

    def queryset(self, request):
        qs = super(ActivityAdmin, self).queryset(request)
        return qs.filter(instance=request.session.get('admin_instance'))
