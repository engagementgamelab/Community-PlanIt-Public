from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import Context, RequestContext, loader
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from web.player_activities.models import *
from web.answers.models import *
from web.missions.models import Mission
from web.instances.models import Instance

from web.processors import instance_processor as ip
from web.player_activities.forms import *
import settings

@login_required
def overview(request, id):
    return HttpResponse("web page not created yet")

@login_required
def get_activity(request, id):
    activity = PlayerActivity.objects.get(id=id)

    if request.method == "POST":
        s = ""
        for x in request.POST:
            s = "%s%s: %s<br>" % (s, x, request.POST[x])
        return HttpResponse(s)
    
        if request.POST["form"] == "open_ended":
            form = OpenForm(request.POST)
            if form.is_valid():
                answer = AnswerOpenEnded.objects.get_or_create(activity=activity, answerUser = request.user)
                answer.answerBox = form.cleaned_data["answerBox"]
                answer.save()
        elif request.POST["form"] == "single_response":
            mc = MultiChoiceActivity.objects.filter(activity=activity)
            choices = []
            for x in mc:
                choices.append((x.id, x.value))
            if settings.DEBUG == True and len(choices) == 0:
                choices.append((1, "Test data"))
                choices.append((2, "More test data"))
                choices.append((3, "This is another test"))
            form = MakeSingleForm(choices)(request.POST)
            if form.is_valid():
                answer = AnswerSingleResponse.objects.get_or_create(activity=activity, answerUser = request.user)
                answer.selected = MultiChoiceActivity.objects.filter(id=int(form.cleaned_data["response"]))
                answer.save()
        elif request.POST["form"] == "map":
            form = MapForm(request.POST)
            if form.is_valid():
                map = form.cleaned_data["map"]
                #typically I would NEVER do this, but this is acceptable here because
                #map is a generated dictionary. I need to take all of the points and put
                #them in as different answers.  
                mapDict = eval(map)
                markers = mapDict["markers"]
                answerBox = form.cleaned_data["answerBox"]
                answer = AnswerMap.objects.get_or_create(activity=activity, answerUser=request.user)
                answer.answerBox = answerBox
                answer.save()
                answer = AnswerMap.objects.get(activity=activity, answerUser=request.user)
                for marker in markers:
                    mapStr = '{"coordinates":%s,"zoom":%s,"markers":[{"coordinates":%s}],"type":"Point"}' % (mapDict["coordinates"], 
                                                                                                             mapDict["zoom"], 
                                                                                                             marker["coordinates"])
                    point = UserMapPoints()
                    point.user = request.user
                    point.map = answer
                    point.point = mapStr
                    point.save()
        elif request.POST["form"] == "empathy":
            form = EmpathyForm(request.POST)
            if form.is_valid():
                answerBox = form.cleaned_data["answerBox"]
                answer = AnswerEmpathy.objects.get_or_create(activity=activity, answerUser=request.user)
                answer.answerBox = answerBox
                answer.save()
        elif request.POST["form"] == "multi_reponse":
            mc = MultiChoiceActivity.objects.filter(activity=activity)
            choices = []
            for x in mc:
                choices.append((x.id, x.value))
            if settings.DEBUG == True and len(choices) == 0:
                choices.append((1, "Test data"))
                choices.append((2, "More test data"))
                choices.append((3, "This is another test"))
            form = MakeMultiForm(choices)(request.POST)
            if form.is_valid():
                #this gets very very messy....
                choices = MultiChoiceActivity.objects.filter(activity=activity)
                ids = []
                for choice in choices:
                    ids.append(choice.id)
                #test for this to delete them all
                AnswerMultiChoice.objects.filter(Q(user=request.user) & Q(option__in=ids))
                if form.cleaned_data.has_key("response_1"):
                    
             
    else:

        tmpl = None
        form = None
        map = None
        if (activity.type.type == "open_ended"):
            tmpl = loader.get_template('player_activities/open_ended.html')
            form = OpenForm()
        elif (activity.type.type == "single_response"):
            tmpl = loader.get_template('player_activities/single_response.html')
            mc = MultiChoiceActivity.objects.filter(activity=activity)
            choices = []
            for x in mc:
                choices.append((x.id, x.value))
            if settings.DEBUG == True and len(choices) == 0:
                choices.append((1, "Test data"))
                choices.append((2, "More test data"))
                choices.append((3, "This is another test"))
            form = MakeSingleForm(choices)
        elif (activity.type.type == "map"):
            activity = PlayerMapActivity.objects.get(pk=activity.id)
            tmpl = loader.get_template('player_activities/map_response.html')
            form = MapForm()
            map = activity.mission.instance.location 
        elif (activity.type.type == "empathy"):
            tmpl = loader.get_template('player_activities/empathy_response.html')
            form = EmpathyForm()
        elif (activity.type.type == "multi_reponse"):
            mc = MultiChoiceActivity.objects.filter(activity=activity)
            choices = []
            for x in mc:
                choices.append((x.id, x.value))
            if settings.DEBUG == True and len(choices) == 0:
                choices.append((1, "Test data"))
                choices.append((2, "More test data"))
                choices.append((3, "This is another test"))
            tmpl = loader.get_template('player_activities/multi_response.html')
            form = MakeMultiForm(choices)
        else:
            raise Http404
        
    return HttpResponse(tmpl.render(RequestContext(request, {
        "form": form, 
        "activity": activity,
        "map": map,
        }, [ip])))
    return HttpResponse("web page not created yet")

@login_required
def index(request):
    user = request.user
    profile = user.get_profile()
    instance = profile.instance
    tmpl = loader.get_template('player_activities/base.html')
    if (instance == None):
        return HttpResponse(tmpl.render(RequestContext(request, {
            'instance': instance,
            'mission': []
        }, [ip])))
        
    missions = Mission.objects.filter(instance=instance).current()
    if (len(missions) == 0):
        return HttpResponse(tmpl.render(RequestContext(request, {
            'instance': instance,
            'mission': []
        }, [ip])))
        
    activities = PlayerActivity.objects.filter(mission=missions[0])
    pks = []
    for pk in Answer.objects.filter(answerUser=request.user):
        pks.append(pk.id)
    #We want to get all activities that the user has for this mission
    #And the user has no answer for
    unfinished_activities = PlayerActivity.objects.filter(Q(mission=missions[0]) & ~Q(pk__in=pks))
    return HttpResponse(tmpl.render(RequestContext(request, {
            'instance': instance,
            'mission': missions[0],
            'activities': activities,
            'unfinished_activities': unfinished_activities,
        }, [ip])))
