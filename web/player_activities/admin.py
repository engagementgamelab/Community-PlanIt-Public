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


class MultiChoiceActivityInline(TranslatableStackedInline):
	model = MultiChoiceActivity

class PlayerActivityAdmin(TranslatableAdmin):
    list_display = ('__str__', 'mission', 'type', 'all_translations')
    list_filter = ('type', 'mission__instance', 'mission', 'is_player_submittd' )
    ordering = ('mission', 'type',)
    inlines = [MultiChoiceActivityInline,]

class PlayerEmpathyActivityAdmin(TranslatableAdmin):
    list_display = ('__str__', 'mission', 'type', 'all_translations')
    list_filter = ('mission', 'type')

class MultiChoiceActivityAdmin(TranslatableAdmin):
    list_display = ('activity', 'activity_type', 'activity_points', 'mission_title', 'all_translations')
    list_filter = ('activity__type', 'trivia_correct_answer')

class PlayerMapActivityAdmin(TranslatableAdmin):
    list_display = ('__str__', 'mission', 'type', 'all_translations')
    list_filter = ('mission__instance', 'mission', 'is_player_submittd' )

admin.site.register(PlayerActivity, PlayerActivityAdmin)
admin.site.register(PlayerActivityType, PlayerActivityTypeAdmin)
admin.site.register(MultiChoiceActivity, MultiChoiceActivityAdmin)
admin.site.register(PlayerMapActivity, PlayerMapActivityAdmin)
admin.site.register(PlayerEmpathyActivity, PlayerEmpathyActivityAdmin)


