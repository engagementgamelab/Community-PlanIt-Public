import urllib
import math
from web.reports.models import Activity
from web.instances.models import PointsAssignment
from django.utils import simplejson
from gmapsfield.fields import GoogleMaps
from django.conf import settings
from django.contrib import messages

class ActivityLogger:
    def log(self, user, request, action, data, url, type):
        if request:
            if user.get_profile().location_tracking and request.COOKIES.has_key('position'):
                try:
                    p = simplejson.loads( urllib.unquote(request.COOKIES.get('position')) )
                    g = GoogleMaps()
                    g.coordinates = [ p.get('coords').get('latitude'), p.get('coords').get('longitude') ]
                    a = Activity(user=user, instance=user.get_profile().instance, action=action, data=data, location=g, url=url, type=type)
                except:
                    a = Activity(user=user, instance=user.get_profile().instance, action=action, data=data, location=None, url=url, type=type)

                a.save()
            else:
                a = Activity(user=user, instance=user.get_profile().instance, action=action, data=data, location=None, url=url, type=type)
                a.save()
        else:
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
        try:
            p = PointsAssignment.objects.get(action=action)
            up = user.get_profile()
            up.points += p.points
            up.coins += p.coins

            if up.points:
                messages.success(request, 'You have earned '+ up.points +' points')

            if up.coins:
                messages.success(request, 'You have earned '+ up.coins +' coins')

        except:
            up = user.get_profile()
            up.points += settings.DEFAULT_POINTS or 10
            up.coins += settings.DEFAULT_COINS or 0
        
        new_coins = 0
        pointDiff = up.points - up.points_multiplier * 100
        #Say points = 480, you make 40 points, you now have 520
        #your multiplier is still 4, 520 - 400 > 100, new coin!
        if pointDiff >= 100:
            new_coins += pointDiff / 100
            up.coins += new_coins
            up.points_multiplier += pointDiff / 100
        up.save()
                
        #if new_coins > 1:
        #    ActivityLogger.log(request.user, request, 'to gain '+ str(up.coins) +' coins', 'earned over '+ str((up.points_multiplier - 1) * 100) +' points', 'issue')
        #else:
        #    ActivityLogger.log(request.user, request, 'to gain a coin', 'earned over '+ str((up.points_multiplier - 1) * 100) +' points', 'issue')

PointsAssigner = PointsAssigner()
