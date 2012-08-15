from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from polymorphic_tree.admin import PolymorphicMPTTParentModelAdmin, PolymorphicMPTTChildModelAdmin

from web.instances.models import *

from . import models as game_models
from web.missions import models as mission_models
from web.challenges import models as challenge_models


# The common admin functionality for all derived models:

class BaseChildAdmin(PolymorphicMPTTChildModelAdmin):
    GENERAL_FIELDSET = (None, {
        'fields': ('parent', 'title'),
    })

    base_model = game_models.BaseTreeNode
    base_fieldsets = (
        GENERAL_FIELDSET,
    )


# Optionally some custom admin code
class AnswerChoiceInline(admin.StackedInline):
	model = challenge_models.AnswerChoice


class ChallengeAdminBase(BaseChildAdmin):
    readonly_fields = ('is_player_submitted', 'created_by')
    exclude = ('challenge_type', 'mission',)

    def save_model(self, request, obj, form, change):
        #TODO should only save these fields
        # if adding a new instance
        if isinstance(obj.parent, mission_models.Mission):
            obj.mission = obj.parent
            obj.created_by = request.user
            obj.save()


class SingleResponseChallengeAdmin(ChallengeAdminBase):
    inlines = [AnswerChoiceInline,]


class MultiResponseChallengeAdmin(ChallengeAdminBase):
    inlines = [AnswerChoiceInline,]


class BarrierChallengeAdmin(ChallengeAdminBase):
    inlines = [AnswerChoiceInline,]


class MapChallengeAdmin(ChallengeAdminBase):
    pass


class EmpathyChallengeAdmin(ChallengeAdminBase):
    pass


class MissionAdmin(BaseChildAdmin):
    #readonly_fields = ('start_date', 'end_date')
    exclude = ('instance', 'start_date', 'end_date')

    def save_model(self, request, obj, form, change):
        #TODO should only save these fields
        # if adding a new instance
        if isinstance(obj.parent, game_models.Instance):
            obj.instance = obj.parent
            obj.save()


class GameAdmin(BaseChildAdmin):
    filter_horizontal = ('curators',)
    #readonly_fields = ('start_date', 'end_date')

# Create the parent admin that combines it all:
class TreeNodeParentAdmin(PolymorphicMPTTParentModelAdmin):
    base_model = game_models.BaseTreeNode
    child_models = (
        (game_models.Instance, GameAdmin),
        (mission_models.Mission, MissionAdmin),
        (challenge_models.SingleResponseChallenge, SingleResponseChallengeAdmin),
        (challenge_models.MultiResponseChallenge, MultiResponseChallengeAdmin),
        (challenge_models.MapChallenge, MapChallengeAdmin),  # custom admin allows custom edit/delete view.
        (challenge_models.EmpathyChallenge, EmpathyChallengeAdmin),
        (challenge_models.BarrierChallenge, BarrierChallengeAdmin),
    )

    list_display = ('title', 'actions_column',)

    class Media:
        css = {
            'all': ('admin/treenode/admin.css',)
        }

    def queryset(self, request):
        qs = super(TreeNodeParentAdmin, self).queryset(request)
        #curators=request.user
        qs = qs.filter()
        return qs
        #from web.instances.models import Instance
        #print request.user
        #return qs.instance_of(Instance)


admin.site.register(game_models.BaseTreeNode, TreeNodeParentAdmin)


"""
from web.accounts.models import UserProfileVariantsForInstance
class UserProfileVariantsForInstanceInline(admin.StackedInline):
    filter_horizontal = ('affiliation_variants', 'stake_variants',)
    model = UserProfileVariantsForInstance

class InstanceAdmin(TranslatableAdmin):
    list_display = ('title', 'start_date', 'city', 'is_disabled')
    list_filter = ('is_disabled',)
    filter_horizontal = ('curators', 'languages',)
    inlines = [
        UserProfileVariantsForInstanceInline,
    ]
class NotificationRequestAdmin(admin.ModelAdmin):
    list_display = ('email', 'instance')

class PointsAssignmentAdmin(admin.ModelAdmin):
    list_display = ('action', 'points', 'instance')

class AffiliationAdmin(admin.ModelAdmin):
	list_display = ('name',)

# Register to admin sites
admin.site.register(Instance, InstanceAdmin)
admin.site.register(Language)
admin.site.register(Affiliation, AffiliationAdmin)
admin.site.register(NotificationRequest, NotificationRequestAdmin)
#admin.site.register(PointsAssignmentAction)
admin.site.register(PointsAssignment, PointsAssignmentAdmin)
"""
