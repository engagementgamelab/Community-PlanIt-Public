import datetime

from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.template import Context, RequestContext, loader

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from web.answers.models import Answer, AnswerMultiChoice
from web.comments.forms import CommentForm
from web.comments.models import Comment
from web.instances.models import Instance
from web.missions.models import *
from web.player_activities.models import PlayerActivity
#from web.processors import instance_processor as ip

@login_required
def fetch(request, slug):
    mission = get_object_or_404(Mission, slug=slug, instance=request.user.get_profile().instance)

    pks = []
    for pk in Answer.objects.filter(answerUser=request.user, activity__mission=mission):
        pks.append(pk.activity.pk)
    
    for mc in AnswerMultiChoice.objects.filter(user=request.user, option__activity__mission=mission):
        pk = mc.option.activity.pk
        if pk not in pks:
            pks.append(pk)
    
    answered_activities = PlayerActivity.objects.filter(Q(pk__in=pks))
    unfinished_activities = PlayerActivity.objects.filter(Q(mission=mission) & ~Q(pk__in=pks))
    
    tmpl = loader.get_template('missions/base.html')
    return HttpResponse(tmpl.render(RequestContext(request, {
        'mission': mission,
        'unfinished_activities': unfinished_activities,
        'answered_activities': answered_activities,
        'comment_form': CommentForm(),
    }, 
    #[ip]
    )))

@login_required
def all(request):
    finished_activities = PlayerActivity.objects.filter(answers__answerUser=request.user)

    tmpl = loader.get_template('missions/all.html')
    return HttpResponse(tmpl.render(RequestContext(request, {
        'played': finished_activities,
    }, 
    #[ip]
    )))
