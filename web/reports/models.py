import datetime

from localeurl.utils import locale_url
from localeurl.templatetags.localeurl_tags import rmlocale

from gmapsfield.fields import GoogleMapsField

from django.dispatch import receiver
from django.db import models
from django.utils import translation
from django.contrib import admin, messages
from django.contrib.auth.models import User

#from reports.signals import log_event
from instances.models import Instance

class Activity(models.Model):
    action = models.CharField(max_length=255)
    data = models.TextField()
    url = models.URLField(blank=True, null=True)
    location = GoogleMapsField(blank=True, null=True) # Make editable false
    date = models.DateTimeField(default=datetime.datetime.now)
    type = models.CharField(max_length=255)

    user = models.ForeignKey(User, blank=True, null=True)
    instance = models.ForeignKey(Instance, blank=True, null=True, editable=False)
    
    class Meta:
        verbose_name = 'Activity'
        verbose_name_plural = 'Activities'

    def __unicode__(self):
        label = self.action +' - '+ self.data
        return label
    
    def get_url(self):
        if self.url:            
            url = rmlocale(self.url)            
            return locale_url(url, translation.get_language())
        return None


class ActivityLogger:
    def log(self, action, data, url, type, instance=None, user=None, request=None):

        if not user:
            user = User.objects.filter(is_superuser=True)[0]
            instance = user.get_profile().instance,

        if not instance:
            instance = Instance.objects.all()[0]

        kwargs = dict(
                user=user,
                instance=instance,
                action=action,
                data=data,
                location=None,
                url=url,
                type=type
        )
        a = Activity.objects.create(**kwargs)
        a.save()

        if request:
            # Push to messages queue
            messages.success(request, 'You ' + data +' '+ action.encode('utf8'))



#from player_activities.models import EmpathyOfficialResponse, MapOfficialResponse, PlayerActivityOfficialResponse
#@receiver(log_event, sender=EmpathyOfficialResponse, dispatch_uid='web.playeractivities.models')
#@receiver(log_event, sender=PlayerActivityOfficialResponse, dispatch_uid='web.playeractivities.models')
#@receiver(log_event, sender=MapOfficialResponse, dispatch_uid='web.playeractivities.models')
#def log_official_response(sender, **kwargs):

#    print kwargs
#    instance = kwargs.pop('instance')
#    action = kwargs.pop('action')
#    data = kwargs.pop('data')
#    url = kwargs.pop('url')
#    type = kwargs.pop('type')

#    ActivityLogger().log(
#            "An official response for activity:: " + instance.activity.name[:30] + "...",
#            data,
#            instance.activity.get_activity_url(),
#            "official_response",
#    )


