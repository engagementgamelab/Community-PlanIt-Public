from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.utils.translation import get_language
from django.utils import simplejson
from django.contrib.auth.decorators import login_required

from player_activities.views import _get_activity, getComments, comment_fun,\
    log_activity
from player_activities.forms import *
from player_activities.models import *
from answers.models import *
from comments.models import *
from comments.forms import *
from reports.actions import *


@login_required
def map_overview(request, id, template='player_activities/map_overview.html'):
    activity = _get_activity(id, PlayerMapActivity)

    comment_form = CommentForm()
    comment_form.allow_replies = False

    context = dict(
            activity = activity,
            comment_form = comment_form,
    )

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

    context.update(dict(
        comments =  getComments(answers, AnswerMap, activity=activity),
        answers = answers,
        init_coords = init_coords,
        map = map,
        myComment = myComment,
        view_action = 'overview',
    ))
    return render_to_response(template, context, RequestContext(request))

@login_required
def map_activity(request, id, template='player_activities/map_response.html'):

    activity = _get_activity(id, PlayerMapActivity)
    init_coords = []
    map = activity.mission.instance.location
    form = MapForm()

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

    answers = AnswerMap.objects.filter(activity=activity, answerUser=request.user)
    if len(answers) > 0:
        return HttpResponseRedirect(reverse("activities:map-replay", args=[activity.id]))

    errors = {}
    if request.method == "POST":
        form = MapForm(request.POST)
        comment_form = CommentForm(request.POST)
        if form.is_valid() and comment_form.is_valid():
            map = form.cleaned_data["map"]
            answer = AnswerMap.objects.create(
                                activity = activity,
                                answerUser = request.user,
                                map = map,
            )
            answer.save()
            PointsAssigner().assignAct(request.user, activity)
            comment_fun(answer, comment_form, request)
            return log_activity(request, activity, "completed", url_reverse="activities:map-overview")
        else:
            if comment_form.errors:
                errors.update(comment_form.errors)
            if form.errors:
                errors.update(form.errors)
    else:
        comment_form = CommentForm(data=request.POST)

    context = dict(
        comment_form = comment_form,
        activity = activity,
        errors = errors,
        init_coords = init_coords,
        map = map,
    )
    return render_to_response(template, RequestContext(request, context))

@login_required
def map_replay(request, id, template='player_activities/map_replay.html'):

    activity = _get_activity(id, PlayerMapActivity)

    form = None
    comment_form = CommentForm()
    init_coords = []
    errors = {}

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

    if request.method == "POST":
        form = MapForm(request.POST)
        if form.is_valid():
            map = form.cleaned_data["map"]
            #try:
            answer = AnswerMap.objects.get(activity=activity, answerUser=request.user)
            answer.map = map;
            answer.save()
            #except AnswerMap.DoesNotExist:
            #    answer = AnswerMap.objects.create(activity=activity, answerUser=request.user, map=map)
            return log_activity(request, activity, "replayed", url_reverse="activities:map-overview")
        else:
            if comment_form.errors:
                errors.update(comment_form.errors)
            if form.errors:
                errors.update(form.errors)

    context = dict(
        form = form, 
        errors = errors,
        activity = activity,
        map = map,
        init_coords = init_coords,
        view_action = 'replay',
    )
    return render_to_response(template, context, RequestContext(request))

