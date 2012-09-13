from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from polymorphic_tree.admin import PolymorphicMPTTChildModelAdmin, PolymorphicMPTTParentModelAdmin

from attachments.models import Attachment

from web.instances.models import *
from web.attachment_types.models import *

from . import models as game_models
from web.missions import models as mission_models
from web.challenges import models as challenge_models

# The common admin functionality for all derived models:


class TreeNodeTypeChoiceForm():
    type_label = _("Tree node type")


class BaseChildAdmin(PolymorphicMPTTChildModelAdmin):
    GENERAL_FIELDSET = (None, {
        'fields': ('parent', 'title'),
    })

    base_model = game_models.BaseTreeNode
    base_fieldsets = (
        GENERAL_FIELDSET,
    )


class AnswerChoiceInline(admin.StackedInline):
    model = challenge_models.AnswerChoice

    def get_formset(self, request, obj=None, **kwargs):
        """ do not display the is_barrier_correct_answer field on challenges that are not Barrier or Final Barrier"""

        if not isinstance(obj, (challenge_models.BarrierChallenge, 
                                challenge_models.FinalBarrierChallenge)):
            if self.exclude is None:
                self.exclude = []
            else:
                self.exclude = list(self.exclude)
            self.exclude.append('is_barrier_correct_answer')
        return super(AnswerChoiceInline, self).get_formset(request, obj=obj, **kwargs)


class ChallengeAdminBase(BaseChildAdmin):
    readonly_fields = ('is_player_submitted', 'created_by',)
    exclude = ('challenge_type', )

    def save_model(self, request, obj, form, change):

        if isinstance(obj, challenge_models.Challenge):
            obj.created_by = request.user
            obj.save()

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, Attachment):
                if isinstance(instance, AttachmentVideo):
                    instance.attachment_file = ''
                instance.creator = request.user
            instance.save()


class SingleResponseChallengeAdmin(ChallengeAdminBase):
    inlines = [AnswerChoiceInline, CPIAttachmentInlines, VideoAttachmentInlines]


class MultiResponseChallengeAdmin(ChallengeAdminBase):
    inlines = [AnswerChoiceInline, CPIAttachmentInlines, VideoAttachmentInlines]


class BarrierChallengeAdmin(ChallengeAdminBase):
    inlines = [AnswerChoiceInline, CPIAttachmentInlines, VideoAttachmentInlines]

    #from django.core.exceptions import ValidationError
    #raise ValidationError("Barrier Challenge must have exactly one correct answer set.")


class FinalBarrierChallengeAdmin(ChallengeAdminBase):
    inlines = [AnswerChoiceInline, CPIAttachmentInlines, VideoAttachmentInlines]


class OpenEndedChallengeAdmin(ChallengeAdminBase):
    inlines = [CPIAttachmentInlines, VideoAttachmentInlines,]


class MapChallengeAdmin(ChallengeAdminBase):
    inlines = [CPIAttachmentInlines, VideoAttachmentInlines,]


class EmpathyChallengeAdmin(ChallengeAdminBase):
    inlines = [CPIAttachmentInlines, VideoAttachmentInlines,]


class MissionAdmin(BaseChildAdmin):
    pass

class GameAdmin(BaseChildAdmin):
    filter_horizontal = ('curators',)
    inlines = [VideoAttachmentInlines,]
    #readonly_fields = ('start_date', 'end_date')


# Create the parent admin that combines it all:
class TreeNodeParentAdmin(PolymorphicMPTTParentModelAdmin):
    base_model = game_models.BaseTreeNode
    #add_type_form = TreeNodeTypeChoiceForm

    # child_models defines:
    #   1) model
    #   2) model admin
    #   3) tuple of models allowed to be the
    #      parent of the current model
    child_models = (
        (game_models.Instance, GameAdmin, ()),
        (mission_models.Mission, MissionAdmin, (game_models.Instance,)),
        (challenge_models.SingleResponseChallenge, SingleResponseChallengeAdmin, (mission_models.Mission,)),
        (challenge_models.MultiResponseChallenge, MultiResponseChallengeAdmin, (mission_models.Mission,)),
        (challenge_models.MapChallenge, MapChallengeAdmin, (mission_models.Mission,)),
        (challenge_models.EmpathyChallenge, EmpathyChallengeAdmin, (mission_models.Mission,)),
        (challenge_models.OpenEndedChallenge, OpenEndedChallengeAdmin, (mission_models.Mission,)),
        (challenge_models.BarrierChallenge, BarrierChallengeAdmin, (mission_models.Mission,)),
        (challenge_models.FinalBarrierChallenge, FinalBarrierChallengeAdmin, (mission_models.Mission,)),
    )
    list_display = ('custom_title', 'actions_column',)

    def custom_title(self, node):
        if isinstance(node.get_real_instance(), challenge_models.Challenge):
            node_type = '[%s]' % node.get_real_instance().get_challenge_type_display()
        elif isinstance(node.get_real_instance(), mission_models.Mission):
            node_type = '[mission]'
        elif isinstance(node.get_real_instance(), game_models.Instance):
            node_type = '[game]'
        else:
            ''
        return u' '.join([node.title, node_type])

    custom_title.allow_tags = True
    custom_title.short_description = _('Title')

    def queryset(self, request):
        qs = super(TreeNodeParentAdmin, self).queryset(request)
        return qs.filter(id__in=
                    [node.pk for node in \
                            filter(lambda n: n.can_create(request.user), qs.filter())]
        )

admin.site.register(game_models.BaseTreeNode, TreeNodeParentAdmin)
