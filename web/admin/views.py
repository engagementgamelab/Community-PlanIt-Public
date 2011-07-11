import datetime
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseServerError
from django.template import Context, RequestContext, loader
from web.instances.models import Instance
from web.processors import instance_processor as ip
from web.admin.forms import *
from django.utils import simplejson

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
                     "init_coords": [],
                     }, [ip])))
            else:
                instance = Instance.objects.get(id=int(form.cleaned_data["instances"]))
                #location = "[42.36475475505694, -71.05134683227556]"
                formEdit = InstanceEditForm(initial={"name": instance.name,
                                                     "start_date": instance.start_date,
                                                     "end_date": instance.end_date,
                                                     })
                markers = simplejson.loads("%s" % instance.location)["markers"]
                x = 0
                init_coords = []
                for coor in markers if markers != None else []:
                    coor = coor["coordinates"]
                    init_coords.append( [x, coor[0], coor[1]] )
                    x = x + 1
                return HttpResponse(tmpl.render(RequestContext(request, { 
                     "new": False, 
                     "form": formEdit, 
                     "instance": instance,
                     "location": instance.location,
                     "init_coords": init_coords,
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
    
    #return HttpResponse(s)

    form = InstanceEditForm(request.POST)
    if form.is_valid():
        for x in form.cleaned_data.keys():
            s = "%s%s: %s (key)<br>" % (s, x, form.cleaned_data[x])
        #return HttpResponse(s)
    
        instance = None
        if request.POST.has_key("instance_id"):
            instance = Instance.objects.get(id=int(request.POST["instance_id"]))
        else:
            instance = Instance()
        
        #return HttpResponse("id: %s <br> instance location %s <br> map %s" % 
        #                    (instance.id, instance.location, form.cleaned_data["map"]))
        
        s = "map: %s <br> %s<br>" % (request.POST["map"], instance.location)
        
        instance.start_date = form.cleaned_data["start_date"]
        instance.end_date = form.cleaned_data["end_date"]
        instance.location = form.cleaned_data["map"]
        instance.curator = request.user
        
        s = "%s %s<br> %s<br>" % (s, instance.location, form.cleaned_data["map"])
        return HttpResponse(s)
        instance.save()
        
        return HttpResponseRedirect("/admin/")
    else:
        location = None
        init_coords = []
        if (request.POST["map"] != ""):
            location = request.POST["map"]
        elif (new):
            location = '{"frozen": null, "zoom": 13, "markers": null, "coordinates": [42.36475475505694, -71.05134683227556], "size": [500, 400]}'
        else:
            instance = Instance.objects.get(id=int(request.POST["instance_id"]))
            location = instance.location
            markers = simplejson.loads("%s" % instance.location)["markers"]
            x = 0
            init_coords = []
            for coor in markers if markers != None else []:
                coor = coor["coordinates"]
                init_coords.append( [x, coor[0], coor[1]] )
                x = x + 1
        
        tmpl = loader.get_template("admin/instance_edit.html")
        return HttpResponse(tmpl.render(RequestContext(request, {
            "new": request.POST.has_key("instance_id"),
            "form": form,
            "location": location,
            "init_coords": init_coords,
            }, [ip])))