from challenges.models import *
from django.contrib import admin

admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(PlayerChallenge)
