from django.shortcuts import render_to_response
from django.template import RequestContext

from web.attachments.models import Attachment

def all(request, template='attachments/index.html'):
    response = {
        'attachments': Attachment.objects.all()
    }
    return render_to_response(template, response, context_instance=RequestContext(request))
    
def instance(request, slug, template='attachments/index.html'):
    response = {}
    return render_to_response(template, response, context_instance=RequestContext(request))