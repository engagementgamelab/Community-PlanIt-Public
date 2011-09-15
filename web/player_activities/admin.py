from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

from nani.admin import TranslatableAdmin, TranslatableStackedInline

from web.player_activities.models import (
    PlayerActivity,
    PlayerActivityType, 
    PlayerMapActivity,
    MultiChoiceActivity,
    PlayerEmpathyActivity, 
)

class PlayerActivityTypeAdmin(ModelAdmin):
    list_display = ('type', 'defaultPoints',)

class PlayerActivityAdmin(TranslatableAdmin):
    list_display = ('__str__', 'mission', 'type', 'all_translations')
    list_filter = ('mission', 'type')
    ordering = ('mission', 'type',)

class PlayerEmpathyActivityAdmin(TranslatableAdmin):
    list_display = ('__str__', 'mission', 'type', 'all_translations')

class MultiChoiceActivityAdmin(TranslatableAdmin):
	list_display = ('activity', 'activity_type', 'activity_points', 'mission_title', 'all_translations')

class PlayerMapActivityAdmin(TranslatableAdmin):
    list_display = ('__str__', 'mission', 'type', 'all_translations')

admin.site.register(PlayerActivity, PlayerActivityAdmin)
admin.site.register(PlayerActivityType, PlayerActivityTypeAdmin)
admin.site.register(MultiChoiceActivity, MultiChoiceActivityAdmin)
admin.site.register(PlayerMapActivity, PlayerMapActivityAdmin)
admin.site.register(PlayerEmpathyActivity, PlayerEmpathyActivityAdmin)
