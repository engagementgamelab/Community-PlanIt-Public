from django.conf import settings
from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render
from django.template import loader, Context, RequestContext
from django.views.decorators.cache import never_cache

from django.contrib.sites.models import Site

from web.accounts.views import dashboard
from web.accounts.forms import AccountAuthenticationForm
from web.instances.models import Instance

def index(request, authentication_form=AccountAuthenticationForm):
    # Show index page
    if not request.user.is_authenticated():
        form = authentication_form(request)
        context = {'form': form}
        return render(request, 'index.html', context)
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
