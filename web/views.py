from django.conf import settings
from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render
from django.template import loader, Context
from django.views.decorators.cache import never_cache
from django.contrib.sites.models import Site

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
