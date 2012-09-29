from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from polymorphic_tree.admin import PolymorphicMPTTChildModelAdmin, PolymorphicMPTTParentModelAdmin

from attachments.models import Attachment
from attachments.admin import AttachmentInlines

from web.instances.models import *
from web.attachment_types.models import *

from . import models as game_models
from web.missions import models as mission_models
from web.challenges import models as challenge_models
from web.causes import models as causes_models

# attachment inlines 
class CPIAttachmentInlines(AttachmentInlines):
    model = Attachment
    readonly_fields = ('creator',)


class AttachmentWithThumbnailInlines(generic.GenericStackedInline):
    model = AttachmentWithThumbnail
    extra = 1
    readonly_fields = ('creator',)


class AttachmentHyperlinkInlines(generic.GenericStackedInline):
    model = AttachmentHyperlink
    extra = 1
    readonly_fields = ('creator',)
    exclude = ('attachment_file',)


class VideoAttachmentInlines(generic.GenericStackedInline):
    model = AttachmentVideo
    extra = 1
    readonly_fields = ('creator',)
    exclude = ('attachment_file',)

# end attachment inlines

class CauseInlines(admin.StackedInline):
    model = causes_models.Cause
    readonly_fields = ('instance',)


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

challenge_base_inlines = [CPIAttachmentInlines, VideoAttachmentInlines, AttachmentHyperlinkInlines, AttachmentWithThumbnailInlines]
challenge_inlines_with_answers = [AnswerChoiceInline, ] + challenge_base_inlines

class SingleResponseChallengeAdmin(ChallengeAdminBase):
    inlines = challenge_inlines_with_answers


class MultiResponseChallengeAdmin(ChallengeAdminBase):
    inlines = challenge_inlines_with_answers


class BarrierChallengeAdmin(ChallengeAdminBase):
    inlines = challenge_inlines_with_answers

    #from django.core.exceptions import ValidationError
    #raise ValidationError("Barrier Challenge must have exactly one correct answer set.")


class FinalBarrierChallengeAdmin(ChallengeAdminBase):
    inlines = challenge_inlines_with_answers


class OpenEndedChallengeAdmin(ChallengeAdminBase):
    inlines = challenge_base_inlines


class MapChallengeAdmin(ChallengeAdminBase):
    inlines = challenge_base_inlines


class EmpathyChallengeAdmin(ChallengeAdminBase):
    inlines = challenge_base_inlines


class MissionAdmin(BaseChildAdmin):
    pass

class GameAdmin(BaseChildAdmin):
    filter_horizontal = ('curators',)
    inlines = [CauseInlines, VideoAttachmentInlines]
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
