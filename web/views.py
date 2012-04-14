from django.conf import settings
from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render, render_to_response
from django.template import loader, Context, RequestContext
from django.views.decorators.cache import never_cache
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.sites.models import Site

from web.accounts.views import dashboard
from web.accounts.forms import AccountAuthenticationForm
from web.instances.models import Instance, City

def index(request, authentication_form=AccountAuthenticationForm, template='index.html'):
    
    domain = request.current_site.domain
    try:
        # City exists, send them to city page
        current_city = City.objects.get(domain=domain)
        # current_city = City.objects.get(pk=2)
        # domain = 'boston.communityplanit.local'
        instances_active = Instance.objects.active_for_city(domain=domain)
        instances_future = Instance.objects.future_for_city(domain=domain)
        instances_past = Instance.objects.past_for_city(domain=domain)
        instances_current = Instance.objects.current_for_city(domain=domain)
        # print instances_current
        template = 'city.html'
        
    except ObjectDoesNotExist:
        # No city, 
        current_city = None
        instances_active = Instance.objects.active()
        instances_future = Instance.objects.future()
        instances_past = Instance.objects.past()
        instances_current = Instance.objects.current()
        # print instances_current
    if not request.user.is_authenticated():

        form = authentication_form(request)
        context = {
            'form': form,
            'current_city': current_city,
            'cities': City.objects.all(),
            'instances_active': instances_active,
            'instances_future': instances_future,
            'instances_past': instances_past,
            'instances_current': instances_current,
        }
        return render_to_response(template, context, context_instance=RequestContext(request))
    
    context = {
        'current_city': current_city,
        'cities': City.objects.all(),
        'instances_active': instances_active,
        'instances_future': instances_future,
        'instances_past': instances_past,
        'instances_current': instances_current,
    }
        
    # return dashboard(request)
    return render_to_response('city.html', context, context_instance=RequestContext(request))

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
