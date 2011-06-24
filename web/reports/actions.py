import urllib
import math
from web.reports.models import Activity
from web.instances.models import PointsAssignment
from django.utils import simplejson
from gmapsfield.fields import GoogleMaps
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, Http404

class ActivityLogger:
    def log(self, user, request, action, data, url, type):
        a = Activity(user=user, instance=user.get_profile().instance, action=action, data=data, location=None, url=url, type=type)
        a.save()

        # Push to messages queue
        messages.success(request, str(data) +' '+ str(action))

ActivityLogger = ActivityLogger()

class PointsAssigner:
    def fetch(self, action):
        p = PointsAssignment.objects.get(action=action)

        return p.points 

    def assign(self, user, action):
        #p = PointsAssignment.objects.get(action=action)
        #return HttpResponse("action: %s, points: %s, coins: %s" % (p.action, p.points, p.coins))
        before = 0
        str = ""
        
        p = PointsAssignment.objects.filter(action=action)
        if len(p) > 0:
            p = p[0]
        else:
            up = user.get_profile()
            up.totalPoints += settings.DEFAULT_POINTS or 10
            up.coinPoints += settings.DEFAULT_POINTS or 10
            up.currentCoins += settings.DEFAULT_COINS or 0
            if up.coinPoints >= 100:
                up.currentCoins += 1
                up.coinPoints = up.coinPoints - 100
            up.save()
            return 
        
        up = user.get_profile()
        up.totalPoints += p.points
        up.coinPoints += p.points
        if up.coinPoints >= 100:
            up.currentCoins += 1
            up.coinPoints = up.coinPoints - 100
        up.save()
                
        #if new_coins > 1:
        #    ActivityLogger.log(request.user, request, 'to gain '+ str(up.coins) +' coins', 'earned over '+ str((up.points_multiplier - 1) * 100) +' points', 'value')
        #else:
        #    ActivityLogger.log(request.user, request, 'to gain a coin', 'earned over '+ str((up.points_multiplier - 1) * 100) +' points', 'value')

PointsAssigner = PointsAssigner()
