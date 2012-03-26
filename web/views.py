from django.conf import settings
from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render_to_response
from django.template import loader, Context, RequestContext
from django.views.decorators.cache import never_cache

from django.contrib.sites.models import Site, RequestSite

from web.accounts.views import dashboard
from web.accounts.forms import AccountAuthenticationForm
from web.instances.models import Instance, City

def index(request, authentication_form=AccountAuthenticationForm):
    # Show index page
    if not request.user.is_authenticated():
        
        form = authentication_form(request)
        context = {
            'form': form,
            'cities': City.objects.all(),
            'instances': Instance.objects.active(),
            'instances_past': Instance.objects.past(),
        }
        return render_to_response('index.html', context, context_instance=RequestContext(request))
    return dashboard(request)

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
