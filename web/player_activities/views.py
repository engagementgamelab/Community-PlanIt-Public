from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import Context, RequestContext, loader
from django.utils import simplejson
from django.shortcuts import render_to_response

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
#from web.processors import instance_processor as ip
from web.reports.actions import *

from PIL import Image

def getComments(answers, ModelType):
    comments = None
    answer_type = ContentType.objects.get_for_model(ModelType)
    for answer in answers:
        if comments == None:
            comments = Comment.objects.filter(content_type=answer_type, object_id=answer.pk)
        else:
            comments = comments | Comment.objects.filter(content_type=answer_type, object_id=answer.pk)
    return comments
        

@login_required
def overview(request, id):
    try:
        activity = PlayerActivity.objects.untranslated().get(id=id)
    except PlayerActivity.DoesNotExist:
        raise Http404 ("PlayerActivity with id %s does not exist" % id)
    if activity.type.type == "open_ended":
        answers = Answer.objects.filter(activity=activity)
        tmpl = loader.get_template('player_activities/open_overview.html')
        comment_form = CommentForm()
        comment_form.allow_replies = False
        myAnswer = Answer.objects.filter(activity=activity, answerUser=request.user)
        myComment = None
        if len(myAnswer) > 0:
            myAnswer = myAnswer[0]
            myComment = myAnswer.comments.all()[0]
        return HttpResponse(tmpl.render(RequestContext(request, {"activity": activity,
                                                                 "answers": answers,
                                                                 "comments": getComments(answers, Answer),
                                                                 "comment_form": comment_form,
                                                                 "myComment": myComment,
                                                                 }, 
                                                                 #[ip]
                                                                 )))
    elif activity.type.type == "single_response":
        answers = AnswerSingleResponse.objects.filter(activity=activity)

        answerDict = {}
        choices = MultiChoiceActivity.objects.filter(activity=activity)
        for choice in choices:
            answerDict[choice.value] = 0

        for answer in answers:
            answerDict[answer.selected.value] = answerDict[answer.selected.value] + 1
    
        answerList = []
        for x in answerDict:
            answerList.append((x, answerDict[x]))
            
        tmpl = loader.get_template('player_activities/single_overview.html')
        comment_form = CommentForm()
        comment_form.allow_replies = False
        myAnswer = AnswerSingleResponse.objects.filter(activity=activity, answerUser=request.user)
        myComment = None
        if len(myAnswer) > 0:
            myAnswer = myAnswer[0]
            myComment = myAnswer.comments.all()[0]
        return HttpResponse(tmpl.render(RequestContext(request, {"activity": activity,
                                                                 "answers": answerList,
                                                                 "comments": getComments(answers, AnswerSingleResponse),
                                                                 "comment_form": comment_form,
                                                                 "myComment": myComment,
                                                                 }, 
                                                                 #[ip]
                                                                 )))
    elif activity.type.type == "multi_response":
        answers = AnswerMultiChoice.objects.filter(option__activity=activity)
        comments = None
        answer_type = ContentType.objects.get_for_model(AnswerMultiChoice)
        
        for answer in answers:
            if comments == None:
                comments = Comment.objects.filter(content_type=answer_type, object_id=answer.pk)
            else:
                comments = comments | Comment.objects.filter(content_type=answer_type, object_id=answer.pk)
        
        myComment = None
        if comments is not None:
            myComment = comments.filter(user=request.user)
        if myComment is not None and len(myComment) > 0:
            myComment = myComment[0]            
        
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
        comment_form = CommentForm()
        comment_form.allow_replies = False
        return HttpResponse(tmpl.render(RequestContext(request, {"activity": activity,
                                                                 "comments": comments,
                                                                 "comment_form": comment_form,
                                                                 "answers": answerList,
                                                                 "myComment": myComment}, 
                                                                 #[ip]
                                                                 )))
    elif activity.type.type == "map":
        answers = AnswerMap.objects.filter(activity=activity)
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

        tmpl = loader.get_template('player_activities/map_overview.html')        
        comment_form = CommentForm()
        comment_form.allow_replies = False
        myAnswer = AnswerMap.objects.filter(activity=activity, answerUser=request.user)
        myComment = None
        if len(myAnswer) > 0:
            myAnswer = myAnswer[0]
            myComment = myAnswer.comments.all()[0]

        return HttpResponse(tmpl.render(RequestContext(request, {"activity": activity,
                                                                 "comments": getComments(answers, AnswerMap),
                                                                 "comment_form": comment_form,
                                                                 "answers": answers,
                                                                 "init_coords": init_coords,
                                                                 "map": map,
                                                                 "myComment": myComment}, 
                                                                #[ip]
                                                                )))
    elif activity.type.type == "empathy":
        activity = PlayerEmpathyActivity.objects.get(id=activity.id)
        answers = Answer.objects.filter(activity=activity)
        tmpl = loader.get_template('player_activities/empathy_overview.html')
        comment_form = CommentForm()
        comment_form.allow_replies = False
        myAnswer = Answer.objects.filter(activity=activity, answerUser=request.user)
        myComment = None
        if len(myAnswer) > 0:
            myAnswer = myAnswer[0]
            myComment = myAnswer.comments.all()[0]
        
        return HttpResponse(tmpl.render(RequestContext(request, {"activity": activity,
                                                                 "comments": getComments(answers, Answer),
                                                                 "comment_form": comment_form,
                                                                 "answers": answers,
                                                                 "myComment": myComment}, 
                                                                 #[ip]
                                                                 )))
    return HttpResponse("web page not created yet")

def comment_fun(answer, form, request):
    comment = answer.comments.create(
        content_object=answer,
        message=form.cleaned_data['message'], 
        user=request.user,
        instance=request.user.get_profile().instance,
    )
    
    if request.POST.has_key('yt-url'):
        if request.POST.get('yt-url'):
            comment.attachment.create(
                    file=None,
                    url=request.POST.get('yt-url'),
                    type='video',
                    user=request.user,
                    instance=request.user.get_profile().instance)
    
    if request.FILES.has_key('picture'):
        file = request.FILES.get('picture')
        picture = Image.open(file)
        if (file.name.rfind(".") -1):
            file.name = "%s.%s" % (file.name, picture.format.lower())
        comment.attachment.create(
            file=request.FILES.get('picture'),
            user=request.user,
            instance=request.user.get_profile().instance)

@login_required
def get_activity(request, id, template=None):
    try:
        activity = PlayerActivity.objects.get(id=id)
    except PlayerActivity.DoesNotExist:
        raise Http404 ("PlayerActivity with id %s does not exist" % id)
    
    answers = Answer.objects.filter(activity=activity, answerUser=request.user)
    if len(answers) > 0:
        return HttpResponseRedirect(reverse("activities:replay", args=[activity.id]))
    answers = AnswerMultiChoice.objects.filter(option__activity=activity, user=request.user)
    if len(answers) > 0:
        return HttpResponseRedirect(reverse("activities:replay", args=[activity.id]))
    
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
        form_error = False 
        comment_form = CommentForm(request.POST)
        if request.POST["form"] == "open_ended":
            if comment_form.is_valid():
                answer = Answer()
                answer.activity = activity
                answer.answerUser = request.user
                answer.save()
                comment_fun(answer, comment_form, request)
            else:
                template =' player_activities/open_response.html'
                form_error = True
        elif request.POST["form"] == "single_response":
            mc = MultiChoiceActivity.objects.filter(activity=activity)
            choices = []
            for x in mc:
                choices.append((x.id, x.value))
            form = MakeSingleForm(choices)(request.POST)
            if form.is_valid() and comment_form.is_valid():
                answer = AnswerSingleResponse()
                answer.activity = activity
                answer.answerUser = request.user
                answer.selected = MultiChoiceActivity.objects.get(id=int(form.cleaned_data["response"]))
                answer.save()
                comment_fun(answer, comment_form, request)
            else:
                template = 'player_activities/single_response.html'
                form_error = True
        elif request.POST["form"] == "map":
            form = MapForm(request.POST)
            if form.is_valid() and comment_form.is_valid():
                map = form.cleaned_data["map"]
                
                answer = AnswerMap()
                answer.activity = activity
                answer.answerUser = request.user
                answer.map = map;
                answer.save()
                comment_fun(answer, comment_form, request)
            else:
                map = request.POST["map"]
                activity = PlayerMapActivity.objects.get(pk=activity.id)
                template = 'player_activities/map_response.html'
                form_error = True
        elif request.POST["form"] == "empathy":
            if comment_form.is_valid():
                answer = Answer()
                answer.activity = activity
                answer.answerUser = request.user
                answer.save()
                comment_fun(answer, comment_form, request)
            else:
                template = 'player_activities/empathy_response.html'
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
                   
                ids = []
                for choice in choices:
                    ids.append(choice.id)
                #cleans out all of the choices that the user selected from the check boxes
                for amc in AnswerMultiChoice.objects.filter(Q(user=request.user) & Q(option__in=ids)):
                    amc.comments.clear()
                AnswerMultiChoice.objects.filter(Q(user=request.user) & Q(option__in=ids)).delete()
                first_found = False 
                for key in request.POST.keys():
                    if key.find("response_") >= 0:
                        answer = AnswerMultiChoice()
                        answer.user = request.user
                        #This is tricky, the reponse: value returned object is response_$(id): id
                        #So basically if the response exists it means that checkbox was checked and the
                        # value returned will be the ID and will always be an int
                        answer.option = MultiChoiceActivity.objects.get(id=int(request.POST[key]))
                        answer.save()
                        #Yes it's a hack, only make a comment for the first response
                        if not first_found:
                            comment_fun(answer, comment_form, request)
                            first_found = True
            else:
                template = 'player_activities/multi_response.html'
                form_error = True
        
        #If the template is None then there wasn't an error so assign the points and redirect
        #Otherwise fall through. Only assign the points if the replay is false, but still redirect
        if form_error == False:
            PointsAssigner().assignAct(request.user, activity)

        if template == None:
            if replay == False:
                ActivityLogger().log(request.user, request, "the activity: " + activity.name[:30] + "...", "completed", reverse("activities:activity", args=[activity.id]), "activity")
            else:
                ActivityLogger().log(request.user, request, "the activity: " + activity.name[:30] + "...", "replayed", reverse("activities:activity", args=[activity.id]), "activity")
            return HttpResponseRedirect(reverse("activities:overview", args=[activity.id]))
    else:
        comment_form = CommentForm()
        if (activity.type.type == "open_ended"):
            template = 'player_activities/open_response.html'
        elif (activity.type.type == "single_response"):
            template = 'player_activities/single_response.html'
            #mc = MultiChoiceActivity.objects.filter(activity=activity)
            #choices = []
            #for x in mc:
            #    choices.append()
            #choices = [(x.id, x.value) for x in MultiChoiceActivity.objects.filter(activity=activity)]
            choices = MultiChoiceActivity.objects.values_list('pk', 'value')
            form = MakeSingleForm(choices)
        elif (activity.type.type == "map"):
            activity = PlayerMapActivity.objects.get(pk=activity.id)
            template = 'player_activities/map_response.html'
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
            answer = AnswerMap.objects.filter(activity=activity, answerUser=request.user)
        elif (activity.type.type == "empathy"):
            activity = PlayerEmpathyActivity.objects.get(pk=activity.id)
            template ='player_activities/empathy_response.html'
        elif (activity.type.type == "multi_response"):
            mc = MultiChoiceActivity.objects.filter(activity=activity)
            choices = []
            for x in mc:
                choices.append((x.id, x.value))
            template = 'player_activities/multi_response.html'
            form = MakeMultiForm(choices)
        else:
            raise Http404
    context = dict(
        form = form, 
        comment_form = comment_form,
        activity =  activity,
        map = map,
        init_coords= init_coords,
    )
    #import ipdb;ipdb.set_trace()
    return render_to_response(template, RequestContext(request, context))

@login_required
def replay(request, id):    
    activity = PlayerActivity.objects.untranslated().get(id=id)
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
        
        form_error = False 
        if request.POST["form"] == "single_response":
            mc = MultiChoiceActivity.objects.filter(activity=activity)
            choices = []
            for x in mc:
                choices.append((x.id, x.value))
            form = MakeSingleForm(choices)(request.POST)
            if form.is_valid():
                try:
                    answer = AnswerSingleResponse.objects.get(activity=activity, answerUser=request.user)
                    answer.selected = MultiChoiceActivity.objects.get(id=int(form.cleaned_data["response"]))
                    answer.save()
                except AnswerSingleResponse.DoesNotExist:
                    answer = AnswerSingleResponse.objects.create(activity=activity, answerUser=request.user,
                                selected = MultiChoiceActivity.objects.get(id=int(form.cleaned_data["response"])))
                
            else:
                tmpl = loader.get_template('player_activities/single_replay.html')
                form_error = True
        elif request.POST["form"] == "map":            
            form = MapForm(request.POST)
            if form.is_valid():
                map = form.cleaned_data["map"]
                try:
                    answer = AnswerMap.objects.get(activity=activity, answerUser=request.user)
                    answer.map = map;
                    answer.save()
                except AnswerMap.DoesNotExist:
                    answer = AnswerMap.objects.create(activity=activity, answerUser=request.user, map=map)
            else:
                map = request.POST["map"]
                activity = PlayerMapActivity.objects.get(pk=activity.id)
                tmpl = loader.get_template('player_activities/map_replay.html')
                form_error = True
        elif request.POST["form"] == "multi_response":
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
                
                comment = None
                delete_answers = []
                for amc in AnswerMultiChoice.objects.filter(Q(user=request.user) & Q(option__in=ids)):
                    if len(amc.comments.all()) > 0:
                        comment = amc.comments.all()[0]
                    delete_answers.append(amc.pk)

                first_found = False 
                for key in request.POST.keys():
                    if key.find("response_") >= 0:
                        answer = AnswerMultiChoice()
                        answer.user = request.user
                        #This is tricky, the reponse: value returned object is response_$(id): id
                        #So basically if the response exists it means that checkbox was checked and the
                        # value returned will be the ID and will always be an int
                        answer.option = MultiChoiceActivity.objects.get(id=int(request.POST[key]))
                        answer.save()
                        #Yes it's a hack, only make a comment for the first response
                        if not first_found:
                            if comment is not None:
                                comment.content_object = answer
                                comment.save()
                            first_found = True
                AnswerMultiChoice.objects.filter(pk__in=delete_answers).delete()
            else:
                tmpl = loader.get_template('player_activities/multi_replay.html')
                form_error = True
        
        #If the template is None then there wasn't an error so assign the points and redirect
        #Otherwise fall through. Only assign the points if the replay is false, but still redirect
        if tmpl == None:
            ActivityLogger().log(request.user, request, "the activity: " + activity.name[:30] + "...", "replayed", reverse("activities:activity", args=[activity.id]), "activity")
            return HttpResponseRedirect(reverse("activities:overview", args=[activity.id]))
    else:
        if (activity.type.type == "single_response"):
            tmpl = loader.get_template('player_activities/single_replay.html')
            mc = MultiChoiceActivity.objects.filter(activity=activity)
            choices = []
            for x in mc:
                choices.append((x.id, x.value))
            form = MakeSingleForm(choices)
        elif (activity.type.type == "map"):
            activity = PlayerMapActivity.objects.untranslated().get(pk=activity.id)
            tmpl = loader.get_template('player_activities/map_replay.html')
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
            answer = AnswerMap.objects.filter(activity=activity, answerUser=request.user)
        elif (activity.type.type == "multi_response"):
            mc = MultiChoiceActivity.objects.filter(activity=activity)
            choices = []
            for x in mc:
                choices.append((x.id, x.value))
            tmpl = loader.get_template('player_activities/multi_replay.html')
            form = MakeMultiForm(choices)
        else:
            raise Http404
    
    return HttpResponse(tmpl.render(RequestContext(request, {
        "form": form, 
        "activity": activity,
        "map": map,
        "init_coords": init_coords,
        }, 
        #[ip]
        )))
    
    

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
        }, 
        #[ip]
        )))

    for mission in instance.missions.all():
        print mission

    missions = instance.missions.active()
    if missions.count() == 0:
        return HttpResponse(tmpl.render(RequestContext(request, {
            'instance': instance,
            'mission': None
        }, 
        #[ip]
        )))
        
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
        }, 
        #[ip]
        )))
