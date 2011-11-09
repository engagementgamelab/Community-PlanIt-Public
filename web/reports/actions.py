import urllib
import math
from gmapsfield.fields import GoogleMaps

from django.utils import simplejson
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, Http404

from instances.models import PointsAssignment 
from reports.models import Activity



class ActivityLogger:
    def log(self, action, data, url, type, instance=None, user=None, request=None):

        if user:
            instance = user.get_profile().instance,

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

class PointsAssigner:
    def fetch(self, action):
        p = PointsAssignment.objects.get(action=action)

        return p.points 
    
    def assignPoints(self, user, points):
        if points == None:
            up = user.get_profile()
            up.totalPoints += settings.DEFAULT_POINTS or 10
            up.coinPoints += settings.DEFAULT_POINTS or 10
            up.currentCoins += settings.DEFAULT_COINS or 0
            if up.coinPoints >= 100:
                up.currentCoins += up.coinPoints / 100
                up.coinPoints = up.coinPoints % 100
            up.save()
        else:
            up = user.get_profile()
            up.totalPoints += points
            up.coinPoints += points
            if up.coinPoints >= 100:
                up.currentCoins += up.coinPoints / 100
                up.coinPoints = up.coinPoints % 100
            up.save()
    
    def assign(self, user, action):
        try:
            p = PointsAssignment.objects.get(instance=user.get_profile().instance, action__action=action)
            self.assignPoints(user, p.points)
        except PointsAssignment.DoesNotExist:
            pass
    
    def assignAct(self, user, activity):
        self.assignPoints(user, activity.getPoints())
