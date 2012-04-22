from django.shortcuts import get_object_or_404, render
from django.template import RequestContext

from .models import Attachment
from web.instances.models import Instance

def index(request, slug=None, template='attachments/index.html', extra_context={}):
    if slug:
        game = get_object_or_404(Instance, slug=slug)
        attachments = Attachment.objects.filter(instance=game, instance__is_disabled=False, is_resource_center=True)
        rc_scope_template_name = 'base_game.html'
    else:
        attachments = Attachment.objects.filter(instance__for_city=request.current_city, instance__is_disabled=False, is_resource_center=True)
        rc_scope_template_name = 'base_game.html'

    context = dict(
            attachments = attachments,
            rc_scope_template_name = rc_scope_template_name,
    )
    if slug:
        context.update({'game': game})

    if extra_context:
        context.update(extra_context)

    return render(request, template, context)

def attachment(request, slug=None, attachment_id=None, template='attachments/attachment.html', extra_context={}):

    attachment = get_object_or_404(Attachment, pk=attachment_id)

    context = dict(
            attachment = attachment,
    )

    if slug is not None :
        game = get_object_or_404(Instance, slug=slug)
        context.update({'game': game})

    if extra_context:
        context.update(extra_context)

    return render(request, template, context)
