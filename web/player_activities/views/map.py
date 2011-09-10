from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.utils.translation import get_language
from django.contrib.auth.decorators import login_required

from player_activities.views import _get_activity, getComments, comment_fun
from player_activities.forms import *
from player_activities.models import *
from answers.models import *
from comments.models import *
from comments.forms import *
from reports.actions import *

@login_required
def map_overview(request, id, template='player_activities/empathy_overview.html'):
    activity = _get_activity(id, PlayerEmpathyActivity)

    """
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
            comments =  getComments(answers, AnswerMap),
            answers = answers,
            init_coords = init_coords,
            map = map,
            myComment = myComment,
        )
    )
    """

    comment_form = CommentForm()
    comment_form.allow_replies = False

    context = dict(
            activity = activity,
            comment_form = comment_form,
    )
    answers = AnswerEmpathy.objects.filter(activity=activity)
    myAnswer = AnswerEmpathy.objects.filter(activity=activity, answerUser=request.user)
    myComment = None
    if len(myAnswer) > 0:
        myAnswer = myAnswer[0]
        myComment = myAnswer.comments.all()[0]

    context.update(
        dict(
            comments =  getComments(answers, AnswerEmpathy),
            answers =  answers,
            myComment =  myComment,
        )
    )
    return render_to_response(template, context, RequestContext(request))

@login_required
def map_activity(request, id, template='player_activities/empathy_response.html'):


    activities = PlayerMapActivity.objects.filter(pk=activity.id)
    if activities.count():
        activity = activities[0]
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

    """
    activity = _get_activity(id, PlayerEmpathyActivity)

    answers = AnswerEmpathy.objects.filter(activity=activity, answerUser=request.user)
    if len(answers) > 0:
        return HttpResponseRedirect(reverse("activities:empathy-replay", args=[activity.id]))

    #answers = AnswerMultiChoice.objects.filter(option__activity=activity, user=request.user)
    #if len(answers) > 0:
    #    return HttpResponseRedirect(reverse("activities:replay", args=[activity.id]))

    errors = {}
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            answer = AnswerEmpathy()
            answer.activity = activity
            answer.answerUser = request.user
            answer.save()
            comment_fun(answer, comment_form, request)
            PointsAssigner().assignAct(request.user, activity)
        else:
            if comment_form.errors:
                errors.update(form.errors)

        #if template == None:
        #    if replay == False:
        #        ActivityLogger().log(request.user, request, "the activity: " + activity.name[:30] + "...", "completed", reverse("activities:activity", args=[activity.id]), "activity")
        #    else:
        #        ActivityLogger().log(request.user, request, "the activity: " + activity.name[:30] + "...", "replayed", reverse("activities:activity", args=[activity.id]), "activity")
        #    return HttpResponseRedirect(reverse("activities:overview", args=[activity.id]))
    else:
        comment_form = CommentForm(data=request.POST)

    print errors

    context = dict(
        comment_form = comment_form,
        activity = activity,
        errors = errors,
    )
    """
    return render_to_response(template, RequestContext(request, context))

@login_required
def map_replay(request, id, template='player_activities/map_replay.html'):

    activity = _get_activity(id, PlayerMapActivity)

    form = None
    comment_form = None

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

    if request.method == "POST":
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
            template = 'player_activities/map_replay.html'
            form_error = True

    context = dict(
        form = form, 
        activity = activity,
    )
    return render_to_response(template, context, RequestContext(request))

