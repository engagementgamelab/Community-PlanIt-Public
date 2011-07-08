import datetime
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseServerError
from django.template import Context, RequestContext, loader
from web.instances.models import Instance
from web.processors import instance_processor as ip
from web.admin.forms import *

def verify(request):
    user = request.user
    if user.is_superuser:
        return None
    else:
        tmpl = loader.get_template("admin/backend_not_superuser.html")
        return HttpResponse(tmpl.render(RequestContext(request, { }, [ip])))

@login_required
def index(request):
    ok = verify(request)
    if ok != None:
        return ok
    tmpl = loader.get_template("admin/backend_index.html")
    return HttpResponse(tmpl.render(RequestContext(request, {
        }, [ip])))

@login_required
def instance_base(request):
    if request.method == 'POST':
        #s = ""
        #for x in request.POST:
        #    s = "%s%s: %s<br>" % (s, x, request.POST[x])
        #return HttpResponse(s)
        if (request.POST["submit_btn"] == "Cancel"):
            return HttpResponseRedirect("/admin/")
        form = InstanceBaseForm(request.POST)
        if form.is_valid():
            tmpl = loader.get_template("admin/instance_edit.html")
            if (form.cleaned_data.has_key("instance_name") and form.cleaned_data["instance_name"] != ""):
                start_date = datetime.datetime.now()
                end_date = start_date + datetime.timedelta(hours=1)
                formEdit = InstanceEditForm(initial={"name": form.cleaned_data["instance_name"],
                                                     "start_date": start_date,
                                                     "end_date": end_date,
                                                      })                
                return HttpResponse(tmpl.render(RequestContext(request, { 
                     "new": True,
                     "form": formEdit,
                     "location": '{"frozen": null, "zoom": 13, "markers": null, "coordinates": [42.36475475505694, -71.05134683227556], "size": [500, 400]}',
                     }, [ip])))
            else:
                instance = Instance.objects.get(id=int(form.cleaned_data["instances"]))
                #location = "[42.36475475505694, -71.05134683227556]"
                formEdit = InstanceEditForm(initial={"name": instance.name,
                                                     "start_date": instance.start_date,
                                                     "end_date": instance.end_date,
                                                     })
                return HttpResponse(tmpl.render(RequestContext(request, { 
                     "new": False, 
                     "form": formEdit, 
                     "instance": instance,
                     "location": instance.location,
                     }, [ip])))
    ok = verify(request)
    if ok != None:
        return ok
    form = InstanceBaseForm()
    tmpl = loader.get_template("admin/instance_base.html")
    return HttpResponse(tmpl.render(RequestContext(request, {
         "form": form,                                            
        }, [ip])))

@login_required
def instance_save(request):
    ok = verify(request)
    if ok != None:
        return ok
    if (request.method != "POST"):
        return HttpResponseServerError("The request method was not POST")
    s = ""
    for x in request.POST:
        s = "%s%s: %s<br>" % (s, x, request.POST[x])
    return HttpResponse(s)

    form = InstanceEditForm(request.POST)
    new = request.POST["submit_btn"] == "Create"
    if form.is_valid():
        return HttpResponse("Here")
    else:
        
        tmpl = loader.get_template("admin/instance_edit.html")
        location = None
        if new:
            location = '{"frozen": null, "zoom": 13, "markers": null, "coordinates": [42.36475475505694, -71.05134683227556], "size": [500, 400]}'
        #else:
            
        return HttpResponse(tmpl.render(RequestContext(request, {
            "new": new,
            "form": form,
            "location": '{"frozen": null, "zoom": 13, "markers": null, "coordinates": [42.36475475505694, -71.05134683227556], "size": [500, 400]}',                                       
            }, [ip])))