from nani.admin import TranslatableAdmin
from django.contrib import admin

from missions.models import Mission

class MissionAdmin(TranslatableAdmin):
    list_display = ('title', 'instance', 'start_date', 'end_date')
    #readonly_fields = ('start_date', 'end_date',)
    list_filter = ('instance__for_city__domain',)


admin.site.register(Mission, MissionAdmin)
