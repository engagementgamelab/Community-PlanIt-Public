from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, Context, RequestContext

from web.accounts.views import dashboard

def index(request):
    # Show index page
    if not request.user.is_authenticated():
        tmpl = loader.get_template('base/index.html')
        return HttpResponse(tmpl.render(RequestContext(request,{})))
    return dashboard(request)

def indexTemp(request):
    # This is the altered temporary index
    if not request.user.is_authenticated():
        tmpl = loader.get_template('base/indexTemp.html')
        return HttpResponse(tmpl.render(RequestContext(request,{})))
    # Show dashboard
    return dashboard(request)

def error_404(request):
    # Show 404 page
    tmpl = loader.get_template('base/404.html')
    return HttpResponse(tmpl.render(RequestContext(request,{})))

def error_500(request):
    # Show 500 page
    tmpl = loader.get_template('base/500.html')
    return HttpResponse(tmpl.render(Context({})))
