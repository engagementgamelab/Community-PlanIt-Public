from django.conf import settings
from django.views.decorators.cache import never_cache
from django.http import HttpResponse, HttpResponseServerError
from django.template import loader, Context, RequestContext

from django.contrib.sites.models import Site

from web.accounts.views import dashboard

def index(request):
    # Show index page
    if not request.user.is_authenticated():
        tmpl = loader.get_template('index.html')
        return HttpResponse(tmpl.render(RequestContext(request,{})))
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
