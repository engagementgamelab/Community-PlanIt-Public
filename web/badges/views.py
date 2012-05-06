from django.shortcuts import render
from web.core.utils import missions_bar_context

def all(request, template='badges/all.html'):
    
    context = {}
    
    context.update(missions_bar_context(request))
    
    return render(request, template, context)