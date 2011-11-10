from django.contrib import admin
from missions.models import *

admin.site.register(Mission, MissionAdmin)
