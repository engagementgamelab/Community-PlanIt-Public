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
from web.comments.models import *
from web.comments.forms import *
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
        answers = Answer.objects.filter(activity=activity)
        tmpl = loader.get_template('player_activities/open_overview.html')
        return HttpResponse(tmpl.render(RequestContext(request, {"activity": activity,
                                                                 "answers": answers,
                                                                 "action": "",
                                                                 "form_value": "open_ended"}, [ip])))
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
        answers = Answer.objects.filter(activity=activity)
        tmpl = loader.get_template('player_activities/empathy_overview.html')
        return HttpResponse(tmpl.render(RequestContext(request, {"activity": activity,
                                                                 "answers": answers}, [ip])))
    return HttpResponse("web page not created yet")

def comment_fun(comment, form, request):
    comment.user = request.user
    comment.instance = request.user.get_profile().instance
    comment.message = form.cleaned_data["message"]
    comment.save()
    
    if request.POST.has_key('yt-url'):
        if request.POST.get('yt-url'):
            comment.attachment.create(
                    file=None,
                    url=request.POST.get('yt-url'),
                    type='video',
                    user=request.user,
                    instance=request.user.get_profile().instance)
    
    if request.FILES.has_key('picture'):
        comment.attachment.create(
            file=request.FILES.get('picture'),
            user=request.user,
            instance=request.user.get_profile().instance)

@login_required
def get_activity(request, id):
    activity = PlayerActivity.objects.get(id=id)
    tmpl = None
    form = None
    comment_form = None
    map = None
    init_coords = []
    if request.method == "POST":
        s = ""
        for x in request.POST.keys():
            s = "%s%s: %s<br>" % (s, x, request.POST[x])
        s = "%s<br> FILES<br>" % s
        for x in request.FILES.keys():
            s = "%s%s: %s" % (s, x, request.FILES[x])
        #return HttpResponse(s)
        
        #If this game is a replay it should be set below. The reason to not check here
        # is because the type of the game might have changed. If that is the case, the Answer.objects.filteer
        # will exist but it will be the wrong one.  
        replay = False
        form_error = False 
        comment_form = CommentForm(request.POST)
        if request.POST["form"] == "open_ended":
            if comment_form.is_valid():
                answer = Answer.objects.filter(activity=activity, answerUser=request.user)
                comment = None
                if (len(answer) > 0):
                    answer = answer[0]
                    replay = True
                    comment = answer.comment
                else:
                    answer = Answer()
                    answer.activity = activity
                    answer.answerUser = request.user
                    comment = Comment()
                comment_fun(comment, comment_form, request)
                answer.comment = comment
                answer.save()
            else:
                tmpl = loader.get_template('player_activities/open_response.html')
                form_error = True
        elif request.POST["form"] == "single_response":
            mc = MultiChoiceActivity.objects.filter(activity=activity)
            choices = []
            for x in mc:
                choices.append((x.id, x.value))
            form = MakeSingleForm(choices)(request.POST)
            if form.is_valid() and comment_form.is_valid():
                answer = AnswerSingleResponse.objects.filter(activity=activity, answerUser = request.user)
                comment = None
                if (len(answer) > 0):
                    answer = answer[0]
                    replay = True
                    comment = answer.comment
                else:
                    answer = AnswerSingleResponse()
                    answer.activity = activity
                    answer.answerUser = request.user
                    comment = Comment()
                comment_fun(comment, comment_form, request)
                answer.selected = MultiChoiceActivity.objects.get(id=int(form.cleaned_data["response"]))
                answer.comment = comment
                answer.save()
            else:
                tmpl = loader.get_template('player_activities/single_response.html')
                form_error = True
        elif request.POST["form"] == "map":
            form = MapForm(request.POST)
            if form.is_valid() and comment_form.is_valid():
                map = form.cleaned_data["map"]
                answer = AnswerMap.objects.filter(activity=activity, answerUser=request.user)
                comment = None
                if (len(answer) > 0):
                    answer = answer[0]
                    replay = True
                    comment = answer.comment
                else:
                    answer = AnswerMap()
                    answer.activity = activity
                    answer.answerUser = request.user
                    comment = Comment()
                comment_fun(comment, comment_form, request)
                answer.map = map;
                answer.comment = comment
                answer.save()
                answer = AnswerMap.objects.get(activity=activity, answerUser=request.user)
            else:
                map = request.POST["map"]
                activity = PlayerMapActivity.objects.get(pk=activity.id)
                tmpl = loader.get_template('player_activities/map_response.html')
                form_error = True
                return HttpResponse("form errors: %s comment errors: %s" % (form.errors, comment_form.errors))
        elif request.POST["form"] == "empathy":
            if comment_form.is_valid():
                answer = Answer.objects.filter(activity=activity, answerUser=request.user)
                comment = None
                if (len(answer) > 0):
                    answer = answer[0]
                    replay = True
                    comment = answer.comment
                else:
                    answer = Answer()
                    answer.activity = activity
                    answer.answerUser = request.user
                    comment = Comment()
                comment_fun(comment, comment_form, request)
                answer.comment = comment
                answer.save()
            else:
                tmpl = loader.get_template('player_activities/empathy_response.html')
                form_error = True
        elif request.POST["form"] == "multi_response":
            mc = MultiChoiceActivity.objects.filter(activity=activity)
            choices = []
            for x in mc:
                choices.append((x.id, x.value))
            form = MakeMultiForm(choices)(request.POST)
            if form.is_valid() and comment_form.is_valid():
                #this gets very very messy....
                choices = MultiChoiceActivity.objects.filter(activity=activity)
                comment = None
                if len(choices) > 0:
                    replay = True
                ids = []
                for choice in choices:
                    ids.append(choice.id)
                #cleans out all of the choices that the user selected from the check boxes
                for amc in AnswerMultiChoice.objects.filter(Q(user=request.user) & Q(option__in=ids)):
                    Comment.objects.filter(pk=amc.comment.pk).delete()
                AnswerMultiChoice.objects.filter(Q(user=request.user) & Q(option__in=ids)).delete()
                comment = Comment()
                comment_fun(comment, comment_form, request)
                for key in request.POST.keys():
                    if key.find("response_") >= 0:
                        answer = AnswerMultiChoice()
                        answer.user = request.user
                        #This is tricky, the reponse: value returned object is response_$(id): id
                        #So basically if the response exists it means that checkbox was checked and the
                        # value returned will be the ID and will always be an int
                        answer.option = MultiChoiceActivity.objects.get(id=int(request.POST[key]))
                        answer.comment = comment
                        answer.save()
            else:
                tmpl = loader.get_template('player_activities/multi_response.html')
                form_error = True
        
        #If the template is None then there wasn't an error so assign the points and redirect
        #Otherwise fall through. Only assign the points if the replay is false, but still redirect
        if replay == False and form_error == False:
            PointsAssigner().assignAct(request.user, activity)

        if tmpl == None:
            return HttpResponseRedirect(reverse('missions_mission', args=[activity.mission.slug]))
    else:
        comment_form = CommentForm()
        if (activity.type.type == "open_ended"):
            tmpl = loader.get_template('player_activities/open_response.html')
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
                form = MapForm()
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
        "comment_form": comment_form,
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
