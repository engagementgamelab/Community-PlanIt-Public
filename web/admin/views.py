import datetime
import re
from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail, send_mass_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseServerError
from django.shortcuts import render_to_response
from django.template import Context, RequestContext, loader
from django.template.defaultfilters import slugify
from django.utils import simplejson
from django.utils.translation import ugettext as _
from web.accounts.models import UserProfile
from web.admin.forms import *
from web.instances.models import Instance
from web.missions.models import Mission
from web.player_activities.models import *
from web.processors import instance_processor as ip
from web.values.models import Value

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
    if request.user.is_superuser:
        instance = Instance.objects.filter(curators=request.user)
        tmpl = loader.get_template("admin/backend_index.html")
        
        return HttpResponse(tmpl.render(RequestContext(request, {
            }, [ip])))
    else:
        instances = Instance.objects.all()
        if request.method == "POST":
            form = StaffBaseForm(request.POST, initial={"instances": instances})
            if form.is_valid():
                player = User.objects.create(email=form.cleaned_data["admin_email"])
                player.first_name = form.cleaned_data["admin_first_name"]
                player.last_name = form.cleaned_data["admin_last_name"]
                player.set_password(form.cleaned_data["admin_temp_pass"])
                player.is_active = True
                player.is_superuser = True
                player.is_staff = True
                player.save()
                uinfo = player.get_profile()
                email_tmpl = None
                body = None
                if form.cleaned_data["instances"] != None:
                    instance = form.cleaned_data["instances"]
                    uinfo.instance = instance
                    instance.curators.add(player)
                    tmpl = loader.get_template('accounts/email/welcome_admin_instance.html')
                    body = tmpl.render(Context({'password': form.cleaned_data["admin_temp_pass"],
                                                'first_name': player.first_name,
                                                'instance': instance }))
                else:
                    tmpl = loader.get_template('accounts/email/welcome_admin_no_instance.html')
                    body = tmpl.render(Context({'password': form.cleaned_data["admin_temp_pass"],
                                                'first_name': player.first_name,}))
                uinfo.save()
                send_mail(_('Welcome to Community PlanIt!'), body, settings.NOREPLY_EMAIL, [player.email], fail_silently=True)
                messages.success(request, _('New admin successfully registered.'))
                
                return HttpResponseRedirect(reverse("admin:admin-base"))
            else:
                tmpl = loader.get_template("admin/backend_staff_index.html")
                return HttpResponse(tmpl.render(RequestContext(request, {
                         "form": form,
                         "instances": instances,
                         }, [ip])))
        else:
            tmpl = loader.get_template("admin/backend_staff_index.html")
            form = StaffBaseForm(initial={"instances": instances})
            return HttpResponse(tmpl.render(RequestContext(request, {
                 "form": form,
                 }, [ip])))
    
@login_required
def instance_initial_index(request):
    ok = verify(request)
    if ok != None:
        return ok

    if request.method == "POST" and request.POST.has_key("continue_btn"):
        form = InstanceEditForm()
        tmpl = loader.get_template("admin/instance_initial_edit.html")
        return HttpResponse(tmpl.render(RequestContext(request, { 
                 "form": form,
                 "location": '{"frozen": null, "zoom": 13, "markers": null, "coordinates": [42.36475475505694, -71.05134683227556], "size": [500, 400]}',
                 "init_coords": [],
                 }, [ip])))
    tmpl = loader.get_template("admin/instance_initial_base.html")
    return HttpResponse(tmpl.render(RequestContext(request, {
        }, [ip])))
    
@login_required
def instance_initial_save(request):
    ok = verify(request)
    if ok != None:
        return ok
    
    if (request.method != "POST"):
        return HttpResponseServerError("The request method was not POST")

    #s = "%s<br>" % request.method
    #for x in request.POST:
    #    s = "%s%s: %s<br>" % (s, x, request.POST[x])
    #return HttpResponse(s)

    
    form = InstanceEditForm(request.POST)
    if form.is_valid():
        instance = Instance()
        instance.name = form.cleaned_data["name"]
        instance.city = form.cleaned_data["city"]
        instance.state = form.cleaned_data["state"]
        instance.start_date = form.cleaned_data["start_date"]
        instance.end_date = None
        instance.location = form.cleaned_data["map"]
        instance.days_for_mission = form.cleaned_data["days_for_mission"]
        instance.save()
        instance.curators.add(request.user)
        tmpl = loader.get_template("admin/value_initial_edit.html")
        return HttpResponse(tmpl.render(RequestContext(request, { 
             "instance_value": instance,
             }, [ip])))
    
    location = None
    init_coords = []
    if (request.POST["map"] != ""):
        location = request.POST["map"]
        markers = simplejson.loads("%s" % instance.location)["markers"]
        x = 0
        init_coords = []
        for coor in markers if markers != None else []:
            coor = coor["coordinates"]
            init_coords.append( [x, coor[0], coor[1]] )
            x = x + 1
    else:
        location = '{"frozen": null, "zoom": 13, "markers": null, "coordinates": [42.36475475505694, -71.05134683227556], "size": [500, 400]}'

    tmpl = loader.get_template("admin/instance_initial_edit.html")
    return HttpResponse(tmpl.render(RequestContext(request, { 
             "form": form,
             "location": location,
             "init_coords": init_coords,
             }, [ip])))

@login_required
def values_initial(request):
    ok = verify(request)
    if ok != None:
        return ok

@login_required
def sendemail(request):
    ok = verify(request)
    if ok != None:
        return ok
    if (request.method != "POST"):
        return HttpResponseServerError("The request method was not POST")
    s = ""
    for x in request.POST:
        s = "%s%s: %s<br>" % (s, x, request.POST[x])
    
    instance = Instance.objects.get(id=int(request.POST["instance_id"]))
    form = InstanceEmailForm(request.POST)
    if form.is_valid():
        body = form.cleaned_data["email"]
        subject = form.cleaned_data["subject"]
        emailList = []
        ups = UserProfile.objects.filter(instance=instance, receive_email=True)
        for up in ups:
            send_mail(subject, body, settings.NOREPLY_EMAIL, [up.user.email], fail_silently=False)
        return HttpResponseRedirect(reverse("admin:admin-base"))
        
    tmpl = loader.get_template("admin/instance_email.html")
    return HttpResponse(tmpl.render(RequestContext(request, { 
             "form": form,
             "instance_value": instance,  
             }, [ip])))

@login_required
def instance_base(request):
    if request.method == 'POST':
        #s = ""
        #for x in request.POST:
        #    s = "%s%s: %s<br>" % (s, x, request.POST[x])
        #return HttpResponse(s)
        
        if (request.POST.has_key("submit_btn") and request.POST["submit_btn"] == "Cancel"):
            return HttpResponseRedirect(reverse("admin:admin-base"))

        form = InstanceBaseForm(request.POST)

        if not form.is_valid():
            print "INVALID FORM:", form
        else:
            print "VALID FORM:", form

            if request.POST.has_key("email_btn"):
                instance = form.cleaned_data["instance"]
                email_form = InstanceEmailForm()
                tmpl = loader.get_template("admin/instance_email.html")
                return HttpResponse(tmpl.render(RequestContext(request, { 
                         "form": email_form,
                         "instance_value": instance,  
                         }, [ip])))
                
            tmpl = loader.get_template("admin/instance_edit.html")
            if (form.cleaned_data.has_key("instance_name") and form.cleaned_data["instance_name"] != ""):
                start_date = datetime.datetime.now()
                formEdit = InstanceEditForm(initial={"name": form.cleaned_data["instance_name"],
                                                     "start_date": start_date,
                                                     "days_for_mission": 7,
                                                      })
                return HttpResponse(tmpl.render(RequestContext(request, { 
                     "new": True,
                     "form": formEdit,
                     "location": '{"frozen": null, "zoom": 13, "markers": null, "coordinates": [42.36475475505694, -71.05134683227556], "size": [500, 400]}',
                     "init_coords": [],
                     }, [ip])))
            else:
                instance = form.cleaned_data["instance"]
                print "INSTANCE:", instance
                #location = "[42.36475475505694, -71.05134683227556]"
                formEdit = InstanceEditForm(initial={"name": instance.name,
                                                     "start_date": instance.start_date,
                                                     "days_for_mission": instance.days_for_mission,
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
        instance.location = form.cleaned_data["map"]
        instance.curator = request.user
        instance.days_for_mission = form.cleaned_data["days_for_mission"]
        instance.save()
        
        missions = Mission.objects.filter(instance=instance)
        x = 0
        lastMission = None
        for mission in missions:
            if x == 0:
                mission.start_date = instance.start_date
            else:
                mission.start_date = lastMission.end_date
            mission.end_date = mission.start_date + datetime.timedelta(days=instance.days_for_mission)
            mission.instance = instance
            mission.save()
            lastMission = mission
        if lastMission != None:
            instance.end_date = lastMission.end_date
        instance.save()
        
        return HttpResponseRedirect(reverse("admin:admin-base"))
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
def instance_manage_base(request):
    temp_instances = Instance.objects.filter(curators=request.user)
    instance_missions = []
    mission_activities = []
    responses = []
    
    instances = []
    missions = []
    activities = []
    responses = []
    for instance in temp_instances:
        instances.append((instance, UserProfile.objects.filter(instance=instance).count()))
        temp_missions = Mission.objects.filter(instance=instance)
        for mission in temp_missions:
            missions.append((instance.pk, mission))
            temp_activities = PlayerActivity.objects.filter(mission=mission)
            for activity in temp_activities:
                if activity.type.type == "map": 
                    activities.append((mission.pk, PlayerMapActivity.objects.get(pk=activity.pk)))
                elif activity.type.type == "empathy":
                    activities.append((mission.pk, PlayerEmpathyActivity.objects.get(pk=activity.pk)))
                elif activity.type.type == "single_response" or activity.type.type == "multi_response":
                    activities.append((mission.pk, activity))
                    choices = MultiChoiceActivity.objects.filter(activity=activity)
                    for choice in choices:
                        responses.append([choice.pk, mission.pk, activity.pk, choice.value])
                else:
                    activities.append((mission.pk, activity))
    types = []
    t = PlayerActivityType.objects.all()
    for type in t:
        types.append(type)
        
    editForm = InstanceEditForm()
    form = InstanceProcessForm()
    tmpl = loader.get_template("admin/instance_manage_base.html")
    return HttpResponse(tmpl.render(RequestContext(request, {
            "single": len(instances) == 1,
            "editForm": editForm,
            "form": form,
            "instances": instances,
            "missions": missions,
            "activities": mission_activities,
            "responses": responses,
            "types": types,
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
            return HttpResponseRedirect(reverse("admin:admin-base"))
        
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
                "instance_value": instance, #can't name it that, that would be bad because it conflicts with ip.instance. call it something like value or soemthing
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
    if (instance_id == ""): 
        return HttpResponseServerError("instance_id not set by POST")
    
    instance = Instance.objects.get(id=int(instance_id))
    Value.objects.filter(instance=instance).delete()
    
    x = 0
    while request.POST.get("value_%s" % x, None) != None and request.POST.get("value_%s" % x) != "":
        value = Value.objects.create(instance=instance, message=request.POST["value_%s" % x])
        x = x + 1
    return HttpResponseRedirect(reverse("admin:admin-base"))

@login_required
def mission_base(request):
    ok = verify(request)
    if ok != None:
        return ok
    instances = Instance.objects.all().order_by("name")
    if request.method == 'POST':
        if (request.POST["submit_btn"] == "Cancel"):
            return HttpResponseRedirect(reverse("admin:admin-base"))
            
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
                "instance_value": instance,
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
        return HttpResponseRedirect(reverse("admin:admin-base"))
    
    
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
        
        #slug testing
        slugs = {}
        for x in toAdd.keys():
            mission, name = toAdd[x]
            if (slugify(name) in slugs):
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
                    "instance_value": instance,
                    "values": index_missions,
                    "slug_error": "Mission name: %s conflicts with mission name: %s" % (name, slugs[slugify(name)])
                    }, [ip])))
            else:
                slugs[slugify(name)] = name
        x = 0
        lastMission = None
        for x in toAdd.keys():
            mission, name = toAdd[x]
            mission.name = name
            if x == 0:
                mission.start_date = instance.start_date
            else:
                mission.start_date = lastMission.end_date
            mission.end_date = mission.start_date + datetime.timedelta(days=instance.days_for_mission)
            mission.instance = instance
            mission.save()
            lastMission = mission
        if lastMission != None:
            instance.end_date = lastMission.end_date
        instance.save()
        return HttpResponseRedirect(reverse("admin:admin-base"))
    
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
        "instance_value": instance,
        "values": index_missions, 
        }, [ip])))
    
@login_required
def activity_base(request):
    ok = verify(request)
    if ok != None:
        return ok
    instances = Instance.objects.all().order_by("name")
    if request.method == 'POST':
        if (request.POST.has_key("submit_btn") and request.POST["submit_btn"] == "Cancel"):
            return HttpResponseRedirect(reverse("admin:admin-base"))
        form = ActivityBaseForm(request.POST, initial={"instances": instances})
        if form.is_valid():
            instance = Instance.objects.get(id=int(form.cleaned_data["instances"]))
            missions = Mission.objects.filter(instance=instance).order_by("start_date")
            index_missions = []
            responses = []
            
            for mission in missions:
                acts = PlayerActivity.objects.filter(mission=mission).order_by("createDate")
                activities = []
                for act in acts:
                    attachment = act.attachment.all().count()
                    if attachment > 0:
                        attachment = act.attachment.all()[0].file
                    else:
                        attachment = None
                    
                    if act.type.type == "map": 
                        activities.append((PlayerMapActivity.objects.get(pk=act.pk), attachment))
                    elif act.type.type == "empathy":
                        activities.append((PlayerEmpathyActivity.objects.get(pk=act.pk), attachment))
                    elif act.type.type == "single_response" or act.type.type == "multi_response":
                        activities.append((act, attachment))
                        choices = MultiChoiceActivity.objects.filter(activity=act)
                        for choice in choices:
                            responses.append([choice.pk, mission.pk, act.pk, choice.value])
                    else:
                        activities.append((act, attachment))
               
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
    form = ActivityBaseForm(initial={"instances": instances})
    tmpl = loader.get_template("admin/activity_base.html")
    return HttpResponse(tmpl.render(RequestContext(request, {
        "form": form,   
        }, [ip])))

def actCopy(copyTo, copyFrom):
    copyTo.name = copyFrom.name
    copyTo.question = copyFrom.question
    copyTo.creationUser = copyFrom.creationUser
    copyTo.mission = copyFrom.mission
    copyTo.type = copyFrom.type
    copyTo.instructions = copyFrom.instructions
    copyTo.addInstructions = copyFrom.addInstructions
    copyTo.points = copyFrom.points

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
    s = "%s FILES: <br> " % s
    for x in request.FILES.keys():
        s = "%s%s: %s<br>" % (s, x, request.FILES[x])
    #return HttpResponse(s)
    
    form = ActivityEditForm(request.POST)
    tmpl = loader.get_template("admin/activity_edit.html")
    
    if (request.POST.has_key("submit_btn") and request.POST["submit_btn"] == "Cancel"):
        return HttpResponseRedirect(reverse("admin:admin-base"))
    
    if form.is_valid():
        activity = None
        type = PlayerActivityType.objects.get(id=int(request.POST["types"]));
        if (request.POST["activity_id"] == "0"):
            if type.type == "map":
                activity = PlayerMapActivity()
            elif type.type == "empathy":
                activity = PlayerEmpathyActivity()
            else: 
                activity = PlayerActivity()
        else:
            activity = PlayerActivity.objects.get(id=int(request.POST["activity_id"]))
            
            #if the current type is single or multi and it's not going to single or multi, delete all of the response choices
            if activity.type.type == "single_response" or activity.type.type == "multi_response":
                if type.type != "single_response" and type.type != "multi_response":
                    MultiChoiceActivity.objects.filter(activity=activity).delete()
            
            #Get the activity as a map or empathy or deal with the change in type
            if activity.type.type == "map" and type.type == "map":
                activity = PlayerMapActivity(pk=activity.pk)
            elif activity.type.type == "empathy" and type.type == "empathy":
                activity = PlayerEmpathyActivity(pk=activity.pk)
            elif activity.type.type != type.type:
                if activity.type.type == "map" and type.type == "empathy":
                    tempAct = PlayerEmpathyActivity()
                    actCopy(tempAct, activity)
                    activity = tempAct
                    PlayerMapActivity.objects.filter(id=int(request.POST["activity_id"])).delete()    
                elif activity.type.type == "map" and type.type != "empathy":
                    tempAct = PlayerActivity()
                    actCopy(tempAct, activity)
                    activity = tempAct
                    PlayerMapActivity.objects.filter(id=int(request.POST["activity_id"])).delete()
                elif activity.type.type == "empathy" and type.type == "map":
                    tempAct = PlayerMapActivity()
                    actCopy(tempAct, activity)
                    activity = tempAct
                    PlayerEmpathyActivity.objects.filter(id=int(request.POST["activity_id"])).delete()    
                elif activity.type.type == "empathy" and type.type != "map":
                    tempAct = PlayerActivity()
                    actCopy(tempAct, activity)
                    activity = tempAct
                    PlayerEmpathyActivity.objects.filter(id=int(request.POST["activity_id"])).delete()
                elif type.type == "map":
                    tempAct = PlayerMapActivity()
                    actCopy(tempAct, activity)
                    activity = tempAct
                    PlayerActivity.objects.filter(id=int(request.POST["activity_id"])).delete()
                elif type.type == "empathy":
                    tempAct = PlayerEmpathyActivity()
                    actCopy(tempAct, activity)
                    activity = tempAct
                    PlayerActivity.objects.filter(id=int(request.POST["activity_id"])).delete()
                    
 
        activity.name = form.cleaned_data["name"]
        activity.question = form.cleaned_data["question"]
        activity.creationUser = request.user
        activity.mission = Mission.objects.get(id=int(request.POST["missions"]))
        activity.type = type
        activity.instructions = form.cleaned_data["instructions"] if form.cleaned_data.has_key("instructions") and form.cleaned_data["instructions"] != "" else None 
        activity.addInstructions = form.cleaned_data["addInstructions"] if form.cleaned_data.has_key("addInstructions") and form.cleaned_data["addInstructions"] != "" else None  
        activity.points = form.cleaned_data["points"] if form.cleaned_data.has_key("points") and form.cleaned_data["points"] != "" else None
        if activity.type.type == "empathy":
            activity.bio  = form.cleaned_data["bio"]
            if request.POST.has_key("clear_avatar") and request.POST.has_key("clear_avatar") == True:
                activity.avatar = None
            if request.FILES.has_key("avatar"):
                activity.avatar = request.FILES["avatar"]
                 
        if activity.type.type == "map":
            activity.maxNumMarkers = form.cleaned_data["maxNumMarkers"]
        activity.save()
        
        
        if request.POST.has_key("clear_attachment") and request.POST.has_key("clear_attachment") == True:
            activity.attachment.clear()
        if request.FILES.has_key("attachment"):
            activity.attachment.clear()
            activity.attachment.create(file=request.FILES.get("attachment"),
                                       user=request.user,
                                       instance=request.user.get_profile().instance)

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
                    response = MultiChoiceActivity.objects.get(pk=response_id)
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
        return HttpResponseRedirect(reverse("admin:admin-base"))     
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
                elif act.type.type == "single_response" or act.type.type == "multi_response":
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

@login_required
def instance_edit(request, instance_id, template="admin/trans_instance_edit.html"):
    try:
	    inst = Instance.objects.untranslated().get(pk=instance_id)
    except Instance.DoesNotExist:
    	raise Http404 ("instance with id %s does not exist" % instance_id)

    errors = []
    if request.method == "POST":
        instance_form = InstanceForm(request.POST, instance=inst)

        if instance_form.is_valid():
            instance = instance_form.save()
            log.debug('hurray!')
            return HttpResponseRedirect(reverse("admin:admin-base"))
        else:
            #for f in instance_form.trans_forms.values():
            #    log.error f.errors
            errors.append("got errors")

    instance_form = InstanceForm(instance=inst)

    markers = simplejson.loads("%s" % inst.location)["markers"]
    x = 0
    init_coords = []
    for coor in markers if markers != None else []:
        coor = coor["coordinates"]
        init_coords.append( [x, coor[0], coor[1]] )
        x = x + 1

    context = {
            'instance_form': instance_form,
            "init_coords": init_coords,
            'new': False,
            'errors': errors,
    }

    return render_to_response(template, RequestContext(request, context))



@login_required
def instance_edit_org(request, instance_id):
    ok = verify(request)
    if ok != None:
        return ok
    
    if (request.POST.has_key("submit_btn") and request.POST["submit_btn"] == "Cancel"):
        return HttpResponseRedirect(reverse("admin-base"))
    
    if request.method == "POST": 
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
            instance.location = form.cleaned_data["map"]
            instance.curator = request.user
            instance.days_for_mission = form.cleaned_data["days_for_mission"]
            instance.save()
            
            missions = Mission.objects.filter(instance=instance)
            x = 0
            lastMission = None
            for mission in missions:
                if x == 0:
                    mission.start_date = instance.start_date
                else:
                    mission.start_date = lastMission.end_date
                mission.end_date = mission.start_date + datetime.timedelta(days=instance.days_for_mission)
                mission.instance = instance
                mission.save()
                lastMission = mission
            if lastMission != None:
                instance.end_date = lastMission.end_date
            instance.save()
            
            return HttpResponseRedirect(reverse("admin:admin-base"))
    
    instance = Instance.objects.get(id=instance_id)
    formEdit = InstanceEditForm(initial={"name": instance.name,
                                         "start_date": instance.start_date,
                                         "days_for_mission": instance.days_for_mission,
                                         })
    markers = simplejson.loads("%s" % instance.location)["markers"]
    x = 0
    init_coords = []
    for coor in markers if markers != None else []:
        coor = coor["coordinates"]
        init_coords.append( [x, coor[0], coor[1]] )
        x = x + 1
    tmpl = loader.get_template("admin/instance_edit_new.html")
    return HttpResponse(tmpl.render(RequestContext(request, { 
         "new": False, 
         "form": formEdit, 
         "instance": instance,
         "location": instance.location,
         "init_coords": init_coords,
         }, [ip])))

@login_required
def instance_email(request, instance_id):
    ok = verify(request)
    if ok != None:
        return ok
    instance = Instance.objects.get(id=instance_id)
    email_form = InstanceEmailForm()
    tmpl = loader.get_template("admin/instance_email.html")
    return HttpResponse(tmpl.render(RequestContext(request, { 
             "form": email_form,
             "instance_value": instance,  
             }, [ip])))

@login_required
def values_edit(request, instance_id):
    ok = verify(request)
    if ok != None:
        return ok
    if request.method == "POST": 
        instance_id = request.POST["instance_id"]
        if (instance_id == ""): 
            return HttpResponseServerError("instance_id not set by POST")
        
        instance = Instance.objects.get(id=int(instance_id))
        Value.objects.filter(instance=instance).delete()
        
        x = 0
        value_ex = re.compile("value_(?P<index_id>\d+)")
        for key in request.POST.keys():
            if value_ex.match(key) != None and request.POST[key] != "":
                value = Value()
                value.instance = instance
                value.message = request.POST[key]
                value.save()
        return HttpResponseRedirect(reverse("admin:admin-base"))

    instance = Instance.objects.get(id=instance_id)
    values = Value.objects.filter(instance=instance)
    index_values = []
    x = 0
    for value in values:
        index_values.append([x, value])
        x = x + 1
    tmpl = loader.get_template("admin/value_edit_new.html")
    return HttpResponse(tmpl.render(RequestContext(request, {
        "instance_value": instance, #can't name it that, that would be bad because it conflicts with ip.instance. call it something like value or soemthing
        "values": index_values, 
        }, [ip])))

@login_required
def mission_order(request, instance_id):
    ok = verify(request)
    if ok != None:
        return ok
    
    if (request.POST.has_key("submit_btn") and request.POST["submit_btn"] == "Cancel"):
        return HttpResponseRedirect(reverse("admin:admin-base"))
    
    if request.method == "POST":
        instance = Instance.objects.get(id=int(request.POST["instance_id"]))
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
        
        #slug testing
        slugs = {}
        for x in toAdd.keys():
            mission, name = toAdd[x]
            if (slugify(name) in slugs):
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
                    "instance_value": instance,
                    "values": index_missions,
                    "slug_error": "Mission name: %s conflicts with mission name: %s" % (name, slugs[slugify(name)])
                    }, [ip])))
            else:
                slugs[slugify(name)] = name
        x = 0
        lastMission = None
        for x in toAdd.keys():
            mission, name = toAdd[x]
            mission.name = name
            if x == 0:
                mission.start_date = instance.start_date
            else:
                mission.start_date = lastMission.end_date
            mission.end_date = mission.start_date + datetime.timedelta(days=instance.days_for_mission)
            mission.instance = instance
            mission.save()
            lastMission = mission
        if lastMission != None:
            instance.end_date = lastMission.end_date
        instance.save()
        return HttpResponseRedirect(reverse("admin:admin-base"))
    instance = Instance.objects.get(id=instance_id)
    missions = Mission.objects.filter(instance=instance).order_by("start_date")
    index_missions = []
    x = 0
    for mission in missions:
        index_missions.append([x, mission])
        x = x + 1
    tmpl = loader.get_template("admin/mission_edit.html")
    return HttpResponse(tmpl.render(RequestContext(request, {
        "instance_value": instance,
        "values": index_missions,
        }, [ip])))


@login_required
def manage_game(request):
    ok = verify(request)
    if ok != None:
        return ok
    #TODO: Make the instances only be drawn from instances that the user supervises
    """
    instance_list = []
    mission_list = []
    activity_list = []
    value_list = []
    instance_missions = []
    mission_activities = []
    
    if request.user.is_superuser:
        instances = Instance.objects.all().order_by("start_date")
    else:
        instances = Instance.objects.filter(curators=request.user).order_by("start_date")
    
    for instance in instances:
        instance_list.append(instance)
        missions = Mission.objects.filter(instance=instance).order_by("start_date")
        for mission in missions:
            mission_list.append(mission)
            instance_missions.append((instance, mission))
            activities = PlayerActivity.objects.filter(mission=mission).order_by("name")
            for activity in activities:
                activity_list.append(activity)
                mission_activities.append((mission, activity))
        values = Value.objects.filter(instance=instance)
        for value in values:
            value_list.append(value)
    """
    #languages = dict(settings.LANGUAGES).keys()
    from nani.utils import get_translation

    if request.user.is_superuser:
        instances = Instance.objects.untranslated().all().order_by("start_date")
    else:
        instances = Instance.objects.untranslated().filter(curators=request.user).order_by("start_date")

    games = {}
    for game in instances:
        games[game] = [get_translation(game, lang) for lang in game.get_available_languages()]
    
    tmpl = loader.get_template("admin/manage_game.html")
    return HttpResponse(tmpl.render(RequestContext(request, {
            'games' : games,
            #"instance_list": instance_list,
            #"mission_list": mission_list,
            #"activity_list": activity_list,
            #"value_list": value_list,
            #"instance_missions": instance_missions,
            #"mission_activities": mission_activities 
            }, [ip])))

def CreateOrUpdateActivity(request):
    form = ActivityEditForm(request.POST)
    tmpl = loader.get_template("admin/activity_edit.html")
    
    if (request.POST.has_key("submit_btn") and request.POST["submit_btn"] == "Cancel"):
        return HttpResponseRedirect(reverse("admin:admin-base"))
    
    if form.is_valid():
        activity = None
        type = PlayerActivityType.objects.get(id=int(request.POST["types"]));
        if (request.POST["activity_id"] == "0"):
            if type.type == "map":
                activity = PlayerMapActivity()
            elif type.type == "empathy":
                activity = PlayerEmpathyActivity()
            else: 
                activity = PlayerActivity()
        else:
            activity = PlayerActivity.objects.get(id=int(request.POST["activity_id"]))
            
            #if the current type is single or multi and it's not going to single or multi, delete all of the response choices
            if activity.type.type == "single_response" or activity.type.type == "multi_response":
                if type.type != "single_response" and type.type != "multi_response":
                    MultiChoiceActivity.objects.filter(activity=activity).delete()
            
            #Get the activity as a map or empathy or deal with the change in type
            if activity.type.type == "map" and type.type == "map":
                activity = PlayerMapActivity(pk=activity.pk)
            elif activity.type.type == "empathy" and type.type == "empathy":
                activity = PlayerEmpathyActivity(pk=activity.pk)
            elif activity.type.type != type.type:
                if activity.type.type == "map" and type.type == "empathy":
                    tempAct = PlayerEmpathyActivity()
                    actCopy(tempAct, activity)
                    activity = tempAct
                    PlayerMapActivity.objects.filter(id=int(request.POST["activity_id"])).delete()    
                elif activity.type.type == "map" and type.type != "empathy":
                    tempAct = PlayerActivity()
                    actCopy(tempAct, activity)
                    activity = tempAct
                    PlayerMapActivity.objects.filter(id=int(request.POST["activity_id"])).delete()
                elif activity.type.type == "empathy" and type.type == "map":
                    tempAct = PlayerMapActivity()
                    actCopy(tempAct, activity)
                    activity = tempAct
                    PlayerEmpathyActivity.objects.filter(id=int(request.POST["activity_id"])).delete()    
                elif activity.type.type == "empathy" and type.type != "map":
                    tempAct = PlayerActivity()
                    actCopy(tempAct, activity)
                    activity = tempAct
                    PlayerEmpathyActivity.objects.filter(id=int(request.POST["activity_id"])).delete()
                elif type.type == "map":
                    tempAct = PlayerMapActivity()
                    actCopy(tempAct, activity)
                    activity = tempAct
                    PlayerActivity.objects.filter(id=int(request.POST["activity_id"])).delete()
                elif type.type == "empathy":
                    tempAct = PlayerEmpathyActivity()
                    actCopy(tempAct, activity)
                    activity = tempAct
                    PlayerActivity.objects.filter(id=int(request.POST["activity_id"])).delete()
                    
 
        activity.name = form.cleaned_data["name"]
        activity.question = form.cleaned_data["question"]
        activity.creationUser = request.user
        activity.type = type
        activity.mission = Mission.objects.get(id=int(request.POST["mission_id"]))
        activity.instructions = form.cleaned_data["instructions"] if form.cleaned_data.has_key("instructions") and form.cleaned_data["instructions"] != "" else None 
        activity.addInstructions = form.cleaned_data["addInstructions"] if form.cleaned_data.has_key("addInstructions") and form.cleaned_data["addInstructions"] != "" else None  
        activity.points = form.cleaned_data["points"] if form.cleaned_data.has_key("points") and form.cleaned_data["points"] != "" else None
        if activity.type.type == "empathy":
            activity.bio  = form.cleaned_data["bio"]
            if request.POST.has_key("clear_avatar") and request.POST.has_key("clear_avatar") == True:
                activity.avatar = None
            if request.FILES.has_key("avatar"):
                activity.avatar = request.FILES["avatar"]
                 
        if activity.type.type == "map":
            activity.maxNumMarkers = form.cleaned_data["maxNumMarkers"]
        activity.save()
        
        
        if request.POST.has_key("clear_attachment") and request.POST.has_key("clear_attachment") == True:
            activity.attachment.clear()
        if request.FILES.has_key("attachment"):
            activity.attachment.clear()
            activity.attachment.create(file=request.FILES.get("attachment"),
                                       user=request.user,
                                       instance=request.user.get_profile().instance)

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
                    response = MultiChoiceActivity.objects.get(pk=response_id)
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
        return HttpResponseRedirect(reverse("admin:admin-base"))     
    else:
        s = ""
        for x in form.errors:
            s = "%s%s: %s<br>" % (s, x, form.errors[x])
        return HttpResponse(s)


@login_required
def activity_new(request, mission_id):
    if (request.POST.has_key("submit_btn") and request.POST["submit_btn"] == "Cancel"):
        return HttpResponseRedirect(reverse("admin:admin-base"))
    
    if request.method == "POST":
        return CreateOrUpdateActivity(request)
    
    mission = Mission.objects.get(id=mission_id)
    types = PlayerActivityType.objects.all()
    editForm = ActivityEditForm()
    tmpl = loader.get_template("admin/activity_edit.html")

    return HttpResponse(tmpl.render(RequestContext(request, {
        "activity": PlayerActivity(),
        "responses": [], 
        "types": types,
        "attachment": None,
        "mission": mission,
        "editForm": editForm,
        }, [ip])))
    
@login_required
def activity_edit(request, mission_id, activity_id):
    if (request.POST.has_key("submit_btn") and request.POST["submit_btn"] == "Cancel"):
        return HttpResponseRedirect(reverse("admin:admin-base"))
    
    if request.method == "POST":
        return CreateOrUpdateActivity(request)

    activity = PlayerActivity.objects.get(id=activity_id)
    mission = Mission.objects.get(id=mission_id)
    if activity.type.type == "map":
        activity = PlayerMapActivity.objects.get(id=activity.id)
    elif activity.type.type == "empathy":
        activity = PlayerEmpathyActivity.objects.get(id=activity.id)
    
    responses = MultiChoiceActivity.objects.filter(activity=activity)
    types = PlayerActivityType.objects.all()
    
    attachment = activity.attachment.all().count()
    if attachment > 0:
        attachment = activity.attachment.all()[0].file
    else:
        attachment = None
    
    editForm = ActivityEditForm()
    tmpl = loader.get_template("admin/activity_edit.html")
    return HttpResponse(tmpl.render(RequestContext(request, {
        "activity": activity,
        "mission": mission,
        "responses": responses, 
        "types": types,
        "attachment": attachment,
        "editForm": editForm,
        }, [ip])))







