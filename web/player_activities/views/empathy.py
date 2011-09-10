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
def empathy_overview(request, id, template='player_activities/empathy_overview.html'):

    activity = _get_activity(id, PlayerEmpathyActivity)

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
def empathy_activity(request, id, template='player_activities/empathy_response.html'):

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
    return render_to_response(template, RequestContext(request, context))

@login_required
def empathy_replay(request, id):    

    activity = _get_activity(id, PlayerEmpathyActivity)

    form = None
    comment_form = None

    raise Http404

    if request.method == "POST":
        raise Http404

    context = dict(
        form = form, 
        activity = activity,
    )
    return render_to_response(template, context, RequestContext(request))
