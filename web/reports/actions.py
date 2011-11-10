from django.conf import settings
from django.contrib.auth.models import User
from stream import utils as stream_utils

from instances.models import PointsAssignment 

"""
        Actor. The object that performed the activity.
        Verb. The verb phrase that identifies the action of the activity.
        Action Object. (Optional) The object linked to the action itself.
        Target. (Optional) The object to which the activity was performed.

example:

    justquick (actor) closed (verb) issue 2 (object) on activity-stream (target) 12 hours ago

----------------------------
User created/update/deleted, accepted/declined, commented ->Challenge (object), on instance (target)
-----------------------------
User replayed/compeleted -> PlayerActivity (object) etc. on mission (target)
-----------------------------
User created OfficialResponse etc.
-----------------------------
User commented/spent_token/reclaimed_token -> Value

"""


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
