from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

from nani.admin import TranslatableAdmin

from web.player_activities.models import (
    PlayerActivity,
    PlayerActivityType, 
    PlayerMapActivity,
    MultiChoiceActivity,
    PlayerEmpathyActivity, 
	PlayerActivityOfficialResponse,
	MapOfficialResponse,
	EmpathyOfficialResponse,
)

class PlayerActivityOfficialResponseInline(admin.StackedInline):
	model = PlayerActivityOfficialResponse

class MapOfficialResponseInline(admin.StackedInline):
	model = MapOfficialResponse

class EmpathyOfficialResponseInline(admin.StackedInline):
	model = EmpathyOfficialResponse

class PlayerActivityTypeAdmin(ModelAdmin):
    list_display = ('type', 'defaultPoints',)

class PlayerActivityAdmin(TranslatableAdmin):
    list_display = ('__str__', 'mission', 'type', 'all_translations')
    list_filter = ('mission', 'type')
    ordering = ('mission', 'type',)
    inlines = [PlayerActivityOfficialResponseInline,]

class PlayerEmpathyActivityAdmin(TranslatableAdmin):
    list_display = ('__str__', 'mission', 'type', 'all_translations')
    inlines = [EmpathyOfficialResponseInline,]

class MultiChoiceActivityAdmin(TranslatableAdmin):
	list_display = ('activity', 'activity_type', 'activity_points', 'mission_title', 'all_translations')

class PlayerMapActivityAdmin(TranslatableAdmin):
    list_display = ('__str__', 'mission', 'type', 'all_translations')
    inlines = [MapOfficialResponseInline,]

admin.site.register(PlayerActivity, PlayerActivityAdmin)
admin.site.register(PlayerActivityType, PlayerActivityTypeAdmin)
admin.site.register(MultiChoiceActivity, MultiChoiceActivityAdmin)
admin.site.register(PlayerMapActivity, PlayerMapActivityAdmin)
admin.site.register(PlayerEmpathyActivity, PlayerEmpathyActivityAdmin)


