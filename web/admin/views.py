import datetime
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseServerError
from django.template import Context, RequestContext, loader
from django.core.urlresolvers import reverse
from web.instances.models import Instance
from web.values.models import Value
from web.missions.models import Mission
from web.player_activities.models import *
from web.processors import instance_processor as ip
from web.admin.forms import *
from django.utils import simplejson
import re
from django.contrib.contenttypes.models import ContentType


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
            return HttpResponseRedirect(reverse("admin-base"))
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
        #for x in form.cleaned_data.keys():
        #    s = "%s%s: %s (key)<br>" % (s, x, form.cleaned_data[x])
        #return HttpResponse(s)
    
        instance = None
        if request.POST.has_key("instance_id"):
            instance = Instance.objects.get(id=int(request.POST["instance_id"]))
        else:
            instance = Instance()
        instance.name = form.cleaned_data["name"]
        instance.start_date = form.cleaned_data["start_date"]
        instance.end_date = form.cleaned_data["end_date"]
        instance.location = form.cleaned_data["map"]
        instance.curator = request.user
        instance.save()
        
        return HttpResponseRedirect(reverse("admin-base"))
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
        
@login_required
def values_base(request):
    instances = Instance.objects.all().order_by("name")
    if request.method == 'POST':
        #s = ""
        #for x in request.POST:
        #    s = "%s%s: %s<br>" % (s, x, request.POST[x])
        #return HttpResponse(s)
        
        if (request.POST["submit_btn"] == "Cancel"):
            return HttpResponseRedirect(reverse("admin-base"))
        
        form = ValueBaseForm(request.POST, initial={"instances": instances})
        if form.is_valid():
            #s = ""
            #for x in form.cleaned_data.keys():
            #    s = "%s%s: %s" % (s, x, form.cleaned_data[x])
            #return HttpResponse("%s" % form.cleaned_data["instances"])
            instance = Instance.objects.get(id=int(form.cleaned_data["instances"]))
            values = Value.objects.filter(instance=instance)
            index_values = []
            x = 0
            for value in values:
                index_values.append([x, value])
                x = x + 1
            tmpl = loader.get_template("admin/value_edit.html")
            return HttpResponse(tmpl.render(RequestContext(request, {
                "instance": instance,
                "values": index_values, 
                }, [ip])))
    
    ok = verify(request)
    if ok != None:
        return ok
    form = ValueBaseForm(initial={"instances": instances})
    tmpl = loader.get_template("admin/value_base.html")
    return HttpResponse(tmpl.render(RequestContext(request, {
        "form": form,   
        }, [ip])))

@login_required
def values_save(request):
    ok = verify(request)
    if ok != None:
        return ok
    if (request.method != "POST"):
        return HttpResponseServerError("The request method was not POST")
    
    instance_id = request.POST["instance_id"]
    instance = Instance.objects.get(id=int(instance_id))
    Value.objects.filter(instance=instance).delete()
    
    x = 0
    while request.POST.get("value_%s" % x, None) != None and request.POST.get("value_%s" % x) != "":
        value = Value()
        value.instance = instance
        value.message = request.POST["value_%s" % x]
        value.save()
        x = x + 1
    return HttpResponseRedirect(reverse("admin-base"))

@login_required
def mission_base(request):
    ok = verify(request)
    if ok != None:
        return ok
    instances = Instance.objects.all().order_by("name")
    if request.method == 'POST':
        if (request.POST["submit_btn"] == "Cancel"):
            return HttpResponseRedirect(reverse("admin-base"))
            
        form = MissionBaseForm(request.POST, initial={"instances": instances})
        if form.is_valid():
            #s = ""
            #for x in form.cleaned_data.keys():
            #    s = "%s%s: %s" % (s, x, form.cleaned_data[x])
            #return HttpResponse("%s" % form.cleaned_data["instances"])
            instance = Instance.objects.get(id=int(form.cleaned_data["instances"]))
            missions = Mission.objects.filter(instance=instance).order_by("start_date")
            index_missions = []
            x = 0
            for mission in missions:
                index_missions.append([x, mission])
                x = x + 1
            tmpl = loader.get_template("admin/mission_edit.html")
            form = MissionSaveForm()
            return HttpResponse(tmpl.render(RequestContext(request, {
                "form": form,                                                    
                "instance": instance,
                "values": index_missions, 
                }, [ip])))
    
    form = MissionBaseForm(initial={"instances": instances})
    tmpl = loader.get_template("admin/mission_base.html")
    return HttpResponse(tmpl.render(RequestContext(request, {
        "form": form,   
        }, [ip])))

@login_required
def mission_save(request):
    ok = verify(request)
    if ok != None:
        return ok
    if (request.method != "POST"):
        return HttpResponseServerError("The request method was not POST")
    
    if (request.POST["submit_btn"] == "Cancel"):
        return HttpResponseRedirect(reverse("admin-base"))
    
    
    instance = Instance.objects.get(id=int(request.POST["instance_id"]))
    form = MissionSaveForm(request.POST)
    if form.is_valid():
        #s = ""
        #for x in form.cleaned_data.keys():
        #    s = "%s%s: %s<br>" % (s, x, form.cleaned_data[x])
        
        #s = "%s Post variables <br>" % s
        #for x in request.POST.keys():
        #    s = "%s%s: %s<br>" % (s, x, request.POST[x])
        #return HttpResponse(s)
        #so the ones to keep are index_X_id_Y where if Y is 0, it's a new one
        # if it's anything else, the mission existed in the db and should be edited
        # index is the index that this mission should be in
        toAdd = {};
        addPat = re.compile("index_(?P<index_id>\d+)_id_(?P<mission_id>\d+)")
        delPat = re.compile("delete_id_(?P<delete_id>\d+)")
        for key in request.POST.keys():
            if addPat.match(key) != None and request.POST[key] != "":
                matchDict = addPat.match(key).groupdict()
                mission_id = int(matchDict["mission_id"])
                mission = None
                if mission_id != 0:
                    mission = Mission.objects.get(id=mission_id)
                else:
                    mission = Mission()
                index_id = int(matchDict["index_id"])
                toAdd[index_id] = (mission, request.POST[key])
            elif delPat.match(key) != None:
                matchDict = delPat.match(key).groupdict()
                delete_id = int(matchDict["delete_id"])
                if delete_id != 0:
                    mission = Mission.objects.get(id=delete_id).delete()

        x = 0
        lastMission = None
        for x in toAdd.keys():
            mission, name = toAdd[x]
            mission.name = name
            if x == 0:
                mission.start_date = instance.start_date
            else:
                mission.start_date = lastMission.end_date
            mission.end_date = mission.start_date + datetime.timedelta(days=form.cleaned_data["days"])
            mission.instance = instance
            mission.save()
            lastMission = mission
        instance.end_date = lastMission.end_date
        instance.save()
        return HttpResponseRedirect(reverse("admin-base"))
    
    
    
    tmpl = loader.get_template("admin/mission_edit.html")
    form = MissionSaveForm(request.POST)
    missions = Mission.objects.filter(instance=instance).order_by("start_date")
    index_missions = []
    x = 0
    for mission in missions:
        index_missions.append([x, mission])
        x = x + 1
    return HttpResponse(tmpl.render(RequestContext(request, {
        "form": form,                                                    
        "instance": instance,
        "values": index_missions, 
        }, [ip])))
    
@login_required
def activity_base(request):
    ok = verify(request)
    if ok != None:
        return ok
    
    if request.method == 'POST':
        if (request.POST.has_key("submit_btn") and request.POST["submit_btn"] == "Cancel"):
            return HttpResponseRedirect(reverse("admin-base"))
        form = ActivityBaseForm(request.POST)
        if form.is_valid():
            instance = Instance.objects.get(id=int(form.cleaned_data["instances"]))
            missions = Mission.objects.filter(instance=instance).order_by("start_date")
            index_missions = []
            responses = []
            
            for mission in missions:
                acts = PlayerActivity.objects.filter(mission=mission).order_by("createDate")
                activities = []
                for act in acts:
                    if act.type.type == "map": 
                        activities.append(PlayerMapActivity.objects.get(pk=act.pk))
                    elif act.type.type == "empathy":
                        activities.append(PlayerEmpathyActivity.objects.get(pk=act.pk))
                    elif act.type.type == "single_response" or act.type.type == "multi_reponse":
                        activities.append(act)
                        choices = MultiChoiceActivity.objects.filter(activity=act)
                        for choice in choices:
                            responses.append([choice.pk, mission.pk, act.pk, choice.value])
                    else:
                        activities.append(act)
               
                index_missions.append([mission, activities])
            
            types = PlayerActivityType.objects.all()
            form = ActivitySaveForm()
            editForm = ActivityEditForm()
            tmpl = loader.get_template("admin/activity_edit.html")
            return HttpResponse(tmpl.render(RequestContext(request, {
                "form": form,
                "editForm": editForm,
                "instance": instance,
                "values": index_missions,
                "list_missions": missions,
                "types": types,
                "responses": responses, 
                }, [ip])))
        
    form = ActivityBaseForm()
    tmpl = loader.get_template("admin/activity_base.html")
    return HttpResponse(tmpl.render(RequestContext(request, {
        "form": form,   
        }, [ip])))
    
@login_required
def activity_save(request):
    ok = verify(request)
    if ok != None:
        return ok
    
    if (request.method != "POST"):
        return HttpResponseServerError("The request method was not POST")
    
    if (not request.POST.has_key("activity_id") or request.POST["activity_id"] == ""):
        return HttpResponseServerError("POST did not contain activity_id")
    
    s = "%s Post variables <br>"
    for x in request.POST.keys():
        s = "%s%s: %s<br>" % (s, x, request.POST[x])
    #return HttpResponse(s)
    
    form = ActivityEditForm(request.POST)
    tmpl = loader.get_template("admin/activity_edit.html")
    
    if (request.POST.has_key("submit_btn") and request.POST["submit_btn"] == "Cancel"):
        return HttpResponseRedirect(reverse("admin-base"))
    
    if form.is_valid():
        activity = None
        if (request.POST["activity_id"] == "0"):
            activity = PlayerActivity()
        else:
            activity = PlayerActivity.objects.get(id=int(request.POST["activity_id"]))
        activity.name = form.cleaned_data["name"]
        activity.question = form.cleaned_data["question"]
        activity.creationUser = request.user
        activity.mission = Mission.objects.get(id=int(request.POST["missions"]))
        activity.type = PlayerActivityType.objects.get(id=int(request.POST["types"]));
        activity.instructions = form.cleaned_data["instructions"] if form.cleaned_data.has_key("instructions") and form.cleaned_data["instructions"] != "" else None 
        activity.addInstructions = form.cleaned_data["addInstructions"] if form.cleaned_data.has_key("addInstructions") and form.cleaned_data["addInstructions"] != "" else None  
        activity.points = form.cleaned_data["points"] if form.cleaned_data.has_key("points") and form.cleaned_data["points"] != "" else None
        activity.save()
        
        #to see what is going on here, look at the mission save
        toAdd = {};
        addPat = re.compile("index_(?P<index_id>\d+)_id_(?P<response_id>\d+)")
        delPat = re.compile("delete_id_(?P<delete_id>\d+)")
        for key in request.POST.keys():
            if addPat.match(key) != None and request.POST[key] != "":
                matchDict = addPat.match(key).groupdict()
                response_id = int(matchDict["response_id"])
                response = None
                if response_id != 0:
                    response = MultiChoiceActivity.objects.get(id=response_id)
                else:
                    response = MultiChoiceActivity()
                    
                index_id = int(matchDict["index_id"])
                toAdd[index_id] = (response, request.POST[key])
            elif delPat.match(key) != None:
                matchDict = delPat.match(key).groupdict()
                delete_id = int(matchDict["delete_id"])
                if delete_id != 0:
                    MultiChoiceActivity.objects.get(id=delete_id).delete()
        #if any form of implementing ordering is required, do it here
        for x in toAdd:
            toAdd[x][0].value = toAdd[x][1]
            toAdd[x][0].activity = activity
            toAdd[x][0].save()
        return HttpResponseRedirect(reverse("admin-base"))     
    else:
        s = ""
        for x in form.errors:
            s = "%s%s: %s<br>" % (s, x, form.errors[x])
        return HttpResponse(s)
        mission = Mission.objects.get(id=int(request.POST["mission_id"]))
        instance = mission.instance
        missions = Mission.objects.filter(instance=instance)
        index_missions = []
        formMission = []
        responses = []
        
        x = 0
        for mission in missions:
            acts = PlayerActivity.objects.filter(mission=mission).order_by("createDate")
            activities = []
            for act in acts:
                if act.type.type == "map": 
                    activities.append(PlayerMapActivity.objects.get(pk=act.pk))
                elif act.type.type == "empathy":
                    activities.append(PlayerEmpathyActivity.objects.get(pk=act.pk))
                elif act.type.type == "single_response" or act.type.type == "multi_reponse":
                    activities.append(act)
                    choices = MultiChoiceActivity.objects.filter(activity=act)
                    for choice in choices:
                        responses.append([choice.pk, mission.pk, act.pk, choice.value])
                else:
                    activities.append(act)
           
            index_missions.append([x, mission, activities])
            x = x + 1
            formMission.append((mission.id, mission.name))
        
        formTypes = []
        types = PlayerActivityType.objects.all()
        for type in types:
            formTypes.append((type.id, type.displayType))
        
        form = ActivitySaveForm(request.POST, initial={"missions": formMission})
        editForm = ActivityEditForm(request.POST, initial={"missions": formMission,
                                             "types": formTypes})
        
        tmpl = loader.get_template("admin/activity_edit.html")
        return HttpResponse(tmpl.render(RequestContext(request, {
            "form": form,
            "editForm": editForm,
            "instance": instance,
            "values": index_missions,
            "types": types,
            "responses": responses, 
            }, [ip]))) 














