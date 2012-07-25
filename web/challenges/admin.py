from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

from nani.admin import TranslatableAdmin, TranslatableStackedInline

from web.challenges.models import *

class ChallengeTypeAdmin(ModelAdmin):
    list_display = ('type', 'defaultPoints',)


class MultiChoiceActivityInline(TranslatableStackedInline):
	model = MultiChoiceActivity

class ChallengeAdmin(TranslatableAdmin):
    list_display = ('__str__', 'mission', 'type', 'points', 'all_translations')
    list_filter = ('type', 'mission__instance', 'mission', 'is_player_submitted' )
    ordering = ('mission', 'type',)
    inlines = [MultiChoiceActivityInline,]

class EmpathyChallengeAdmin(TranslatableAdmin):
    list_display = ('__str__', 'mission', 'type', 'all_translations')
    list_filter = ('mission', 'type')

class MultiChoiceActivityAdmin(TranslatableAdmin):
    list_display = ('activity', 'activity_type', 'activity_points', 'mission_title', 'all_translations')
    list_filter = ('activity__type', 'trivia_correct_answer')

class MapChallengeAdmin(TranslatableAdmin):
    list_display = ('__str__', 'mission', 'type', 'all_translations')
    list_filter = ('mission__instance', 'mission', 'is_player_submitted' )

admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(ChallengeType, ChallengeTypeAdmin)
admin.site.register(MultiChoiceActivity, MultiChoiceActivityAdmin)
admin.site.register(MapChallenge, MapChallengeAdmin)
admin.site.register(EmpathyChallenge, EmpathyChallengeAdmin)

admin.site.register(Answer)
admin.site.register(AnswerEmpathy)
admin.site.register(AnswerSingleResponse)
admin.site.register(AnswerOpenEnded)

class AnswerMapAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'activity', 'user_name')
    
    def user_name(self, obj):
        return obj.answerUser.get_profile() and obj.answerUser.get_profile().screen_name or answerUser.answerUsername

admin.site.register(AnswerMap, AnswerMapAdmin)

class AnswerMultiChoiceAdmin(admin.ModelAdmin):

    list_display = ('__str__', 'activity', 'user_name')
    list_filter = ('option__activity__mission', 'option__activity__mission__instance',)
    search_fields = ('option__activity__name', )

    def activity(self, obj):
        return unicode(obj.option.activity.name)

    def user_name(self, obj):
        return obj.user.get_profile() and obj.user.get_profile().screen_name or user.username

admin.site.register(AnswerMultiChoice, AnswerMultiChoiceAdmin)


