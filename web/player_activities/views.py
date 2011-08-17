from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import Context, RequestContext, loader
from django.utils import simplejson

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from web.answers.models import *
from web.instances.models import Instance
from web.missions.models import Mission
from web.player_activities.forms import *
from web.player_activities.models import *
from web.processors import instance_processor as ip
from web.reports.actions import *

@login_required
def overview(request, id):
    activity = PlayerActivity.objects.get(id=id)
    
    answerStr = ""
    
    if activity.type.type == "open_ended":
        answers = AnswerOpenEnded.objects.filter(activity=activity)
        tmpl = loader.get_template('player_activities/open_overview.html')
        return HttpResponse(tmpl.render(RequestContext(request, {"activity": activity,
                                                                 "answers": answers}, [ip])))
    elif activity.type.type == "single_response":
        answers = AnswerSingleResponse.objects.filter(activity=activity)
        answerDict = {}
        choices = MultiChoiceActivity.objects.filter(activity=activity)
        for choice in choices:
            answerDict[choice.value] = 0

        for answer in answers:
            answerDict[choice.value] = answerDict[choice.value] + 1
        
        answerList = []
        for x in answerDict:
            answerList.append((x, answerDict[x]))
            
        tmpl = loader.get_template('player_activities/single_overview.html')
        return HttpResponse(tmpl.render(RequestContext(request, {"activity": activity,
                                                                 "answers": answerList}, [ip])))
    elif activity.type.type == "multi_response":
        answers = AnswerMultiChoice.objects.filter(option__activity=activity)
        answerDict = {}
        choices = MultiChoiceActivity.objects.filter(activity=activity)
        for choice in choices:
            answerDict[choice.value] = 0

        for answer in answers:
            answerDict[answer.option.value] = answerDict[answer.option.value] + 1
        
        answerList = []
        for x in answerDict:
            answerList.append((x, answerDict[x]))
            
        tmpl = loader.get_template('player_activities/single_overview.html')
        return HttpResponse(tmpl.render(RequestContext(request, {"activity": activity,
                                                                 "answers": answerList}, [ip])))
    elif activity.type.type == "map":
        answers = AnswerMap.objects.filter(activity=activity)
        tmpl = loader.get_template('player_activities/map_overview.html')
        init_coords = []
        x = 0
        for answer in answers:
            map = answer.map
            markers = simplejson.loads("%s" % map)["markers"]
            for coor in markers if markers != None else []:
                coor = coor["coordinates"]
                init_coords.append( [x, coor[0], coor[1]] )
                x = x + 1
        map = activity.mission.instance.location
        return HttpResponse(tmpl.render(RequestContext(request, {"activity": activity,
                                                                 "answers": answers,
                                                                 "init_coords": init_coords,
                                                                 "map": map}, [ip])))
    elif activity.type.type == "empathy":
        answers = AnswerEmpathy.objects.filter(activity=activity)
        tmpl = loader.get_template('player_activities/empathy_overview.html')
        return HttpResponse(tmpl.render(RequestContext(request, {"activity": activity,
                                                                 "answers": answers}, [ip])))
    return HttpResponse("web page not created yet")

@login_required
def get_activity(request, id):
    activity = PlayerActivity.objects.get(id=id)
    tmpl = None
    form = None
    map = None
    init_coords = []
    if request.method == "POST":
        
        s = ""
        for x in request.POST.keys():
            s = "%s%s: %s" % (s, x, request.POST[x])
        #return HttpResponse(s)
        
        #If this game is a replay it should be set below. The reason to not check here
        # is because the type of the game might have changed. If that is the case, the Answer.objects.filteer
        # will exist but it will be the wrong one.  
        replay = False 

        if request.POST["form"] == "open_ended":
            form = OpenForm(request.POST)
            if form.is_valid():
                answer = AnswerOpenEnded.objects.filter(activity=activity, answerUser=request.user)
                if (len(answer) > 0):
                    answer = answer[0]
                    replay = True
                else:
                    answer = AnswerOpenEnded()
                    answer.activity = activity
                    answer.answerUser = request.user
                answer.answerBox = form.cleaned_data["answerBox"]
                answer.save()
            else:
                tmpl = loader.get_template('player_activities/open_response.html')
        elif request.POST["form"] == "single_response":
            mc = MultiChoiceActivity.objects.filter(activity=activity)
            choices = []
            for x in mc:
                choices.append((x.id, x.value))
            form = MakeSingleForm(choices)(request.POST)
            if form.is_valid():
                answer = AnswerSingleResponse.objects.filter(activity=activity, answerUser = request.user)
                if (len(answer) > 0):
                    answer = answer[0]
                    replay = True
                else:
                    answer = AnswerSingleResponse()
                    answer.activity = activity
                    answer.answerUser = request.user
                answer.selected = MultiChoiceActivity.objects.get(id=int(form.cleaned_data["response"]))
                answer.save()
            else:
                tmpl = loader.get_template('player_activities/single_response.html')
        elif request.POST["form"] == "map":
            form = MapForm(request.POST)
            if form.is_valid():
                map = form.cleaned_data["map"]
                answerBox = form.cleaned_data["answerBox"]
                answer = AnswerMap.objects.filter(activity=activity, answerUser=request.user)
                if (len(answer) > 0):
                    answer = answer[0]
                    replay = True
                else:
                    answer = AnswerMap()
                    answer.activity = activity
                    answer.answerUser = request.user
                answer.answerBox = answerBox
                answer.map = map;
                answer.save()
                answer = AnswerMap.objects.get(activity=activity, answerUser=request.user)
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
                    replay = True
                else:
                    answer = AnswerEmpathy()
                    answer.activity = activity
                    answer.answerUser = request.user
                answer.answerBox = answerBox
                answer.save()
            else:
                tmpl = loader.get_template('player_activities/empathy_response.html')
        elif request.POST["form"] == "multi_response":
            mc = MultiChoiceActivity.objects.filter(activity=activity)
            choices = []
            for x in mc:
                choices.append((x.id, x.value))
            form = MakeMultiForm(choices)(request.POST)
            if form.is_valid():
                #this gets very very messy....
                choices = MultiChoiceActivity.objects.filter(activity=activity)
                if len(choices) > 0:
                    replay = True
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
            else:
                tmpl = loader.get_template('player_activities/multi_response.html')
        
        #If the template is None then there wasn't an error so assign the points and redirect
        #Otherwise fall through. Only assign the points if the replay is false, but still redirect
        if replay == False:
            PointsAssigner().assignAct(request.user, activity)

        if tmpl == None:
            return HttpResponseRedirect(reverse('missions_mission', args=[activity.mission.slug]))
    else:
        if (activity.type.type == "open_ended"):
            tmpl = loader.get_template('player_activities/open_response.html')
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
            answer = AnswerMap.objects.filter(activity=activity, answerUser=request.user)
            if (len(answer) > 0):
                form = MapForm(initial={"answerBox": answer[0].answerBox})
                map = answer[0].map
                markers = simplejson.loads("%s" % map)["markers"]
                x = 0
                for coor in markers if markers != None else []:
                    coor = coor["coordinates"]
                    init_coords.append( [x, coor[0], coor[1]] )
                    x = x + 1
            else:
                map = activity.mission.instance.location
                form = MapForm()
        
        elif (activity.type.type == "empathy"):
            activity = PlayerEmpathyActivity.objects.get(pk=activity.id)
            tmpl = loader.get_template('player_activities/empathy_response.html')
            form = EmpathyForm()
        elif (activity.type.type == "multi_response"):
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
        "init_coords": init_coords,
        }, [ip])))
    return HttpResponse("web page not created yet")

@login_required
def index(request):
    user = request.user
    profile = user.get_profile()
    instance = profile.instance
    tmpl = loader.get_template('player_activities/index.html')
    if (instance == None):
        return HttpResponse(tmpl.render(RequestContext(request, {
            'instance': instance,
            'mission': []
        }, [ip])))
        
    missions = instance.missions.active()
    if missions.count() == 0:
        return HttpResponse(tmpl.render(RequestContext(request, {
            'instance': instance,
            'mission': None
        }, [ip])))
        
    activities = PlayerActivity.objects.filter(mission=missions[0])
    pks = []
    for pk in Answer.objects.filter(answerUser=request.user, activity__mission=missions[0]):
        pks.append(pk.activity.pk)
    
    for mc in AnswerMultiChoice.objects.filter(user=request.user, option__activity__mission=missions[0]):
        pk = mc.option.activity.pk
        if pk not in pks:
            pks.append(pk)
    
    answered_activities = PlayerActivity.objects.filter(Q(pk__in=pks))
    
    #We want to get all activities that the user has for this mission
    #And the user has no answer for
    unfinished_activities = PlayerActivity.objects.filter(Q(mission=missions[0]) & ~Q(pk__in=pks))
    return HttpResponse(tmpl.render(RequestContext(request, {
            'instance': instance,
            'mission': missions[0],
            'activities': activities,
            'unfinished_activities': unfinished_activities,
        }, [ip])))
