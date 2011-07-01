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
    tmpl = None
    form = None
    map = None
    if request.method == "POST":
        #s = ""
        #for x in request.POST:
        #    s = "%s%s: %s<br>" % (s, x, request.POST[x])
        #return HttpResponse(s)
        
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
            form = MakeSingleForm(choices)(request.POST)
            if form.is_valid():
                answer = AnswerSingleResponse.objects.get_or_create(activity=activity, answerUser = request.user)
                answer.selected = MultiChoiceActivity.objects.filter(id=int(form.cleaned_data["response"]))
                answer.save()
        elif request.POST["form"] == "map":
            form = MapForm(request.POST)
            if form.is_valid():
                map = form.cleaned_data["map"]
                answerBox = form.cleaned_data["answerBox"]
                answer = AnswerMap.objects.filter(activity=activity, answerUser=request.user)
                if (len(answer) > 0):
                    answer = answer[0]
                else:
                    answer = AnswerMap()
                    answer.activity = activity
                    answer.answerUser = request.user
                answer.answerBox = answerBox
                answer.map = map;
                answer.save()
                answer = AnswerMap.objects.get(activity=activity, answerUser=request.user)
                return HttpResponseRedirect('/dashboard/')
            else:
                map = request.POST["map"]
                activity = PlayerMapActivity.objects.get(pk=activity.id)
                tmpl = loader.get_template('player_activities/map_response.html')
        elif request.POST["form"] == "empathy":
            form = EmpathyForm(request.POST)
            if form.is_valid():
                answerBox = form.cleaned_data["answerBox"]
                answer = AnswerEmpathy.objects.filter(activity=activity, answerUser=request.user)
                if (len(answer) > 0):
                    answer = answer[0]
                else:
                    answer = AnswerEmpathy()
                    answer.activity = activity
                    answer.answerUser = request.user
                answer.answerBox = answerBox
                answer.save()
                return HttpResponseRedirect('/dashboard/')
            else:
                tmpl = loader.get_template('player_activities/empathy_response.html')
        elif request.POST["form"] == "multi_reponse":
            mc = MultiChoiceActivity.objects.filter(activity=activity)
            choices = []
            for x in mc:
                choices.append((x.id, x.value))
            form = MakeMultiForm(choices)(request.POST)
            if form.is_valid():
                #this gets very very messy....
                choices = MultiChoiceActivity.objects.filter(activity=activity)
                ids = []
                for choice in choices:
                    ids.append(choice.id)
                #cleans out all of the choices that the user selected from the check boxes
                AnswerMultiChoice.objects.filter(Q(user=request.user) & Q(option__in=ids)).delete()
                for key in request.POST.keys():
                    if key.find("response_") >= 0:
                        answer = AnswerMultiChoice()
                        answer.user = request.user
                        #This is tricky, the reponse: value returned object is response_$(id): id
                        #So basically if the response exists it means that checkbox was checked and the
                        # value returned will be the ID and will always be an int
                        answer.option = MultiChoiceActivity.objects.get(id=int(request.POST[key]))
                        answer.save()
                return HttpResponseRedirect('/dashboard/')
            else:
                tmpl = loader.get_template('player_activities/multi_response.html')
    else:
        if (activity.type.type == "open_ended"):
            tmpl = loader.get_template('player_activities/open_ended.html')
            form = OpenForm()
        elif (activity.type.type == "single_response"):
            tmpl = loader.get_template('player_activities/single_response.html')
            mc = MultiChoiceActivity.objects.filter(activity=activity)
            choices = []
            for x in mc:
                choices.append((x.id, x.value))
            form = MakeSingleForm(choices)
        elif (activity.type.type == "map"):
            activity = PlayerMapActivity.objects.get(pk=activity.id)
            tmpl = loader.get_template('player_activities/map_response.html')
            form = MapForm()
            map = activity.mission.instance.location 
        elif (activity.type.type == "empathy"):
            activity = PlayerEmpathyActivity.objects.get(pk=activity.id)
            tmpl = loader.get_template('player_activities/empathy_response.html')
            form = EmpathyForm()
        elif (activity.type.type == "multi_reponse"):
            mc = MultiChoiceActivity.objects.filter(activity=activity)
            choices = []
            for x in mc:
                choices.append((x.id, x.value))
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
