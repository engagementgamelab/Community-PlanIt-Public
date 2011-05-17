from django.contrib import admin
from web.missions.models import *

admin.site.register(Mission, MissionAdmin)
