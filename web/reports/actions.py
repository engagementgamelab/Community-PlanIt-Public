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
            up.save()

            if up.points:
                messages.success(request, 'You have earned '+ up.points +' points')

            if up.coins:
                messages.success(request, 'You have earned '+ up.coins +' coins')

        except:
            up = user.get_profile()
            up.points += settings.DEFAULT_POINTS or 10
            up.coins += settings.DEFAULT_COINS or 0
            up.save()

        if up.points > 0:
            if up.points_multiplier == 0:
                up.points_multiplier = 1

            if up.points >= up.points_multiplier * 99:
                up.points_multiplier += math.floor(up.points / (up.points_multiplier*99))
                up.coins += math.floor(up.points / ((up.points_multiplier - 1) * 99))
                up.save()

        offset = up.points_multiplier or 1
        if up.points >= offset * 99:
            new_coins = math.floor(up.points / (offset * 99))
            up.coins += new_coins
            up.points_multiplier = offset + new_coins
            up.save()

            if new_coins > 1:
                ActivityLogger.log(request.user, request, 'to gain '+ str(up.coins) +' coins', 'earned over '+ str((up.points_multiplier - 1) * 100) +' points', 'issue')
            else:
                ActivityLogger.log(request.user, request, 'to gain a coin', 'earned over '+ str((up.points_multiplier - 1) * 100) +' points', 'issue')

PointsAssigner = PointsAssigner()
