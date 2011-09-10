from operator import itemgetter

from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.utils.translation import get_language
from django.contrib.auth.decorators import login_required

from player_activities.views import _get_activity, getComments, comment_fun, process_comment
from player_activities.forms import *
from player_activities.models import *
from answers.models import *
from comments.models import *
from comments.forms import *
from reports.actions import *
from django.contrib.auth.models import User

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

    activities = PlayerActivity.objects.filter(id=id)

    if activities.count():
        activity = activities[0]
    else:
        raise Http404 ("PlayerActivity with id %s does not exist" % id)

    comment_form = process_comment(request, activity)

    comment_form = CommentForm()
    comment_form.allow_replies = False

    context = dict(
            activity = activity,
            comment_form = comment_form,
    )

    if activity.type.type == "open_ended":
        answers = Answer.objects.filter(activity=activity)
        myAnswer = Answer.objects.filter(activity=activity, answerUser=request.user)
        myComment = None
        if len(myAnswer) > 0:
            myAnswer = myAnswer[0]
            myComment = myAnswer.comments.all()[0]
        template = 'player_activities/open_overview.html'

        context.update(
            dict(
                answers = answers,
                comments = getComments(answers, Answer),
                myComment = myComment
            )
        )

    elif activity.type.type == "single_response":
        answers = AnswerSingleResponse.objects.filter(activity=activity)

        answerDict = {}
        choices = MultiChoiceActivity.objects.language(get_language()).filter(activity=activity)
        for choice in choices:
            answerDict[choice.value] = 0

        for answer in answers:
            answerDict[answer.selected.value] = answerDict[answer.selected.value] + 1

        answerList = []
        for x in answerDict:
            answerList.append((x, answerDict[x]))
        answerList = sorted(answerList, key=itemgetter(1))
        myAnswer = AnswerSingleResponse.objects.filter(activity=activity, answerUser=request.user)
        myComment = None
        if myAnswer.count() > 0:
            myAnswer = myAnswer[0]
            comments = myAnswer.comments.all()
            if comments.count():
                myComment = comments[0]

        template = 'player_activities/single_overview.html'
        context.update(
            dict(
                answers = answerList,
                comments = getComments(answers, AnswerSingleResponse),
                myComment = myComment,
            )
        )

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
        choices = MultiChoiceActivity.objects.language(get_language()).filter(activity=activity)
        for choice in choices:
            answerDict[choice.value] = 0

        for answer in answers:
            answerDict[answer.option.value] = answerDict[answer.option.value] + 1

        answerList = []
        for x in answerDict:
            answerList.append((x, answerDict[x]))

        template = 'player_activities/single_overview.html'
        context.update(
            dict(
                comments = comments,
                answers = answerList,
                myComment = myComment,
            )
        )

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

        myAnswer = AnswerMap.objects.filter(activity=activity, answerUser=request.user)
        myComment = None
        if len(myAnswer) > 0:
            myAnswer = myAnswer[0]
            myComment = myAnswer.comments.all()[0]

        template = 'player_activities/map_overview.html'
        context.update(
            dict(
                comments = getComments(answers, AnswerMap),
                answers = answers,
                init_coords = init_coords,
                map = map,
                myComment = myComment,
            )
        )

    elif activity.type.type == "empathy":
        peactivities = PlayerEmpathyActivity.objects.language(get_language()).filter(id=activity.id)
        if peactivities.count():
            activity = peactivities[0]
        answers = Answer.objects.filter(activity=activity)
        myAnswer = Answer.objects.filter(activity=activity, answerUser=request.user)
        myComment = None
        if len(myAnswer) > 0:
            myAnswer = myAnswer[0]
            myComment = myAnswer.comments.all()[0]

        template = 'player_activities/empathy_overview.html'
        context.update(
            dict(
                comments = getComments(answers, Answer),
                answers = answers,
                myComment = myComment,
            )
        )
    if context and template:
        return render_to_response(template, context, RequestContext(request))
    return HttpResponse("web page not created yet")

@login_required
def activity(request, id, template=None):

    activity = _get_activity(id, PlayerActivity)
    #import ipdb;ipdb.set_trace()

    #answers = Answer.objects.filter(activity=activity, answerUser=request.user)
    #if len(answers) > 0:
    #    return HttpResponseRedirect(reverse("activities:replay", args=[activity.id]))

    #answers = AnswerMultiChoice.objects.filter(option__activity=activity, user=request.user)
    #if len(answers) > 0:
    #    return HttpResponseRedirect(reverse("activities:replay", args=[activity.id]))

    comment_form = CommentForm()
    form = None

    if (activity.type.type == "open_ended"):
        template = 'player_activities/open_response.html'

    elif (activity.type.type == "single_response"):
        template = 'player_activities/single_response.html'
        choices = MultiChoiceActivity.objects.language(get_language()).filter(activity=activity).values_list('pk', 'value')
        form = make_single_form(choices)

    elif (activity.type.type == "multi_response"):
        template = 'player_activities/multi_response.html'
        choices = MultiChoiceActivity.objects.language(get_language()).filter(activity=activity).values_list('pk', 'value')
        form = make_multi_form(choices)

    else:
        raise Http404

    if request.method == "POST":
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
                template = 'player_activities/open_response.html'
                form_error = True

        elif request.POST["form"] == "single_response":
            mc = MultiChoiceActivity.objects.language(get_language()).filter(activity=activity).order_by('id')
            choices = []
            for x in mc:
                choices.append((x.id, x.value))
            form = make_single_form(choices)(request.POST)
            if form.is_valid() and comment_form.is_valid():
                answer = AnswerSingleResponse()
                answer.activity = activity
                answer.answerUser = request.user
                mcactivities = MultiChoiceActivity.objects.filter(id=int(form.cleaned_data["response"]))
                if mcactivities.count():
                    answer.selected = mcactivities[0]
                answer.save()
                comment_fun(answer, comment_form, request)
            else:
                template = 'player_activities/single_response.html'
                form_error = True

        elif request.POST["form"] == "multi_response":
            mc = MultiChoiceActivity.objects.language(get_language()).filter(activity=activity).order_by('id')
            choices = []
            for x in mc:
                choices.append((x.id, x.value))
            form = make_multi_form(choices)(request.POST)
            if form.is_valid() and comment_form.is_valid():
                #this gets very very messy....
                choices = MultiChoiceActivity.objects.language(get_language()).filter(activity=activity).order_by('id')
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
                        answer.option = MultiChoiceActivity.objects.language(get_language()).get(
                                                                        id=int(request.POST[key])
                        )
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
    context = dict(
        form = form, 
        comment_form = comment_form,
        activity =  activity,
    )
    return render_to_response(template, RequestContext(request, context))

@login_required
def replay(request, id):    
    activity = PlayerActivity.objects.get(id=id)
    tmpl = None
    form = None
    comment_form = None

    if (activity.type.type == "single_response"):
        template = 'player_activities/single_replay.html'
        mc = MultiChoiceActivity.objects.filter(activity=activity)
        choices = []
        for x in mc:
            choices.append((x.id, x.value))
        form = make_single_form(choices)

    elif (activity.type.type == "multi_response"):
        mc = MultiChoiceActivity.objects.filter(activity=activity)
        choices = []
        for x in mc:
            choices.append((x.id, x.value))
        template = 'player_activities/multi_replay.html'
        form = make_multi_form(choices)

    else:
        raise Http404
    

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
            form = make_single_form(choices)(request.POST)
            if form.is_valid():
                try:
                    answer = AnswerSingleResponse.objects.get(activity=activity, answerUser=request.user)
                    answer.selected = MultiChoiceActivity.objects.get(id=int(form.cleaned_data["response"]))
                    answer.save()
                except AnswerSingleResponse.DoesNotExist:
                    answer = AnswerSingleResponse.objects.create(activity=activity, answerUser=request.user,
                                selected = MultiChoiceActivity.objects.get(id=int(form.cleaned_data["response"])))
            else:
                template = 'player_activities/single_replay.html'
                form_error = True

        elif request.POST["form"] == "multi_response":
            mc = MultiChoiceActivity.objects.filter(activity=activity)
            choices = []
            for x in mc:
                choices.append((x.id, x.value))
            form = make_multi_form(choices)(request.POST)
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
                template = 'player_activities/multi_replay.html'
                form_error = True
        
        #If the template is None then there wasn't an error so assign the points and redirect
        #Otherwise fall through. Only assign the points if the replay is false, but still redirect
        if tmpl == None:
            ActivityLogger().log(request.user, request, "the activity: " + activity.name[:30] + "...", "replayed", reverse("activities:activity", args=[activity.id]), "activity")
            return HttpResponseRedirect(reverse("activities:overview", args=[activity.id]))

    context = dict(
        form = form, 
        activity = activity,
    )
    return render_to_response(template, context, RequestContext(request))

