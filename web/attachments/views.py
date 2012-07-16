from django.shortcuts import get_object_or_404, render
from django.template import RequestContext

from .models import Attachment
from web.instances.models import Instance
from web.core.utils import missions_bar_context

def index(request, slug=None, template='attachments/index.html', extra_context={}):
    context = {}
    
    if slug:
        game = get_object_or_404(Instance, slug=slug)
        attachments = Attachment.objects.filter(instance=game, instance__is_disabled=False, is_resource_center=True)
    else:
        attachments = Attachment.objects.filter(instance__for_city=request.current_city, instance__is_disabled=False, is_resource_center=True)

    context.update({
        'attachments': attachments,
    })

    if extra_context:
        context.update(extra_context)

    context.update(missions_bar_context(request))
    return render(request, template, context)

def post_game(request, template='attachments/post_game.html', extra_context={}):
    context = {}
    
    attachments = Attachment.objects.filter(instance__for_city=request.current_city, instance__is_disabled=False, is_post_game=True)
    
    context.update({
        'attachments': attachments,
    })

    context.update(missions_bar_context(request))
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
    context.update(missions_bar_context(request))
    return render(request, template, context)
