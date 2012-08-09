#from django.contrib import admin
#from django.contrib.admin.options import ModelAdmin
#from web.challenges.models import *

#from django.utils.translation import ugettext_lazy as _
#from polymorphic_tree.admin import PolymorphicMPTTParentModelAdmin, PolymorphicMPTTChildModelAdmin
#from . import models


"""
# The common admin functionality for all derived models:

class BaseChildAdmin(PolymorphicMPTTChildModelAdmin):
    GENERAL_FIELDSET = (None, {
        'fields': ('parent', 'title'),
    })

    base_model = models.BaseTreeNode
    base_fieldsets = (
        GENERAL_FIELDSET,
    )


# Optionally some custom admin code
class AnswerChoiceInline(admin.StackedInline):
	model = models.AnswerChoice


class TextNodeAdmin(BaseChildAdmin):
    inlines = [AnswerChoiceInline,]


# Create the parent admin that combines it all:

class TreeNodeParentAdmin(PolymorphicMPTTParentModelAdmin):
    base_model = models.BaseTreeNode
    child_models = (
        (models.Challenge, BaseChildAdmin),
        (models.MapChallenge, TextNodeAdmin),  # custom admin allows custom edit/delete view.
        (models.EmpathyChallenge, BaseChildAdmin),
    )

    list_display = ('title', 'actions_column',)

    class Media:
        css = {
            'all': ('admin/treenode/admin.css',)
        }

admin.site.register(models.BaseTreeNode, TreeNodeParentAdmin)


class MultiChoiceActivityInline(TranslatableStackedInline):
	model = MultiChoiceActivity

class ChallengeAdmin(TranslatableAdmin):
    list_display = ('__str__', 'mission', 'challenge_type', 'points', 'all_translations')
    list_filter = ('challenge_type', 'mission__instance', 'mission', 'is_player_submitted' )
    ordering = ('mission', 'type',)
    inlines = [MultiChoiceActivityInline,]
    exclude = ('type', 'points', 'creationUser',)
    #readonly_fields = ()

class EmpathyChallengeAdmin(TranslatableAdmin):
    list_display = ('__str__', 'mission', 'type', 'all_translations')
    list_filter = ('mission', 'type')
    exclude = ('attachment', 'type', )

class MapChallengeAdmin(TranslatableAdmin):
    list_display = ('__str__', 'mission', 'type', 'all_translations')
    list_filter = ('mission__instance', 'mission', 'is_player_submitted' )
    exclude = ('attachment', 'type')

class MultiChoiceActivityAdmin(TranslatableAdmin):
    list_display = ('activity', 'activity_type', 'activity_points', 'mission_title', 'all_translations')
    list_filter = ('activity__type', 'trivia_correct_answer')


admin.site.register(Challenge, ChallengeAdmin)
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
"""



