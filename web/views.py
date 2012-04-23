from django.conf import settings
from django.http import HttpResponse, HttpResponseServerError, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader, Context
from django.views.decorators.cache import never_cache
from django.contrib.sites.models import Site
from django import forms
from django.core.mail import send_mail

from web.settings import *
from web.accounts.views import dashboard
from web.accounts.forms import AccountAuthenticationForm
from web.instances.models import Instance, City

def index(request, authentication_form=AccountAuthenticationForm, template='index.html'):

    domain = request.current_site.domain
    print domain
    try:
        current_city = City.objects.get(domain=domain)
    except City.DoesNotExist:
        # No city,
        current_city = None
    else:
        # City exists, send them to city page
        template = 'city.html'

    context = dict(
        instances_past = Instance.objects.past(for_city=current_city),
        instances_active = Instance.objects.active(for_city=current_city),
        instances_future = Instance.objects.future(for_city=current_city),
        instances_current = Instance.objects.current(for_city=current_city),
        current_city = current_city,
        cities = City.objects.all(),
    )
    if not request.user.is_authenticated():
        context.update({
            'form': authentication_form(request),
        })
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
