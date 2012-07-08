from django.conf import settings
from django.http import HttpResponse, HttpResponseServerError, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader, Context
from django.views.decorators.cache import never_cache
from django.contrib.sites.models import Site
from django import forms
from django.core.mail import send_mail

from web.settings import *
from web.missions.models import Mission
from web.accounts.forms import AccountAuthenticationForm
from web.accounts.models import UserProfilePerInstance
from web.instances.models import Instance, City
from web.core.utils import missions_bar_context

import logging
log = logging.getLogger(__name__)

def index(request, template='index.html', city_header=True):
    context = {
        'instances': Instance.objects.all(),
        'instances_past': Instance.objects.past(),
        'instances_active': Instance.objects.active(),
        'instances_future': Instance.objects.future(),
        'instances_current': Instance.objects.current(),
    }
    context.update({
        'city_header': city_header
    })
    if hasattr(request, 'current_game'): 
        context.update(missions_bar_context(request))
    
    return render(request, template, context)

class BringCpiForm(forms.Form):
    name = forms.CharField(max_length=255)
    email = forms.EmailField()
    role = forms.CharField(max_length=255)
    message = forms.CharField(widget=forms.Textarea)

def bringcpi(request, template='bringcpi.html'):
    if request.method == 'POST': 
        form = BringCpiForm(request.POST)
        if form.is_valid(): 
            
            message = 'From %s: <%s>\n%s\n%s' % (form.cleaned_data['name'], form.cleaned_data['email'], form.cleaned_data['role'], form.cleaned_data['message'])
            
            send_mail('Bring CommunityPlanIt to You submissions', message, settings.NOREPLY_EMAIL,
                settings.BRINGCPI_RECIPIENTS, fail_silently=False)
                
            return HttpResponseRedirect('/bring-cpi-to-you/thanks/')
    else:
        form = BringCpiForm()

    context = {
        'form': form,
        'cities': City.objects.all(),
    }
    
    if hasattr(request, 'current_game'): 
        context.update(missions_bar_context(request))
    return render(request, template, context)

@never_cache
def server_error(request, template_name='500.html'):
    t = loader.get_template(template_name)
    return HttpResponseServerError(
        t.render(
            Context({
                'MEDIA_URL': settings.MEDIA_URL,
                'site': Site.objects.get_current()
            })
        )
    )
