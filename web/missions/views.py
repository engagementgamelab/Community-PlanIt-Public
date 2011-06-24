import datetime
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import Context, RequestContext, loader
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from web.missions.models import *
from web.instances.models import Instance
from web.comments.models import Comment
from web.comments.forms import CommentForm
from web.answers.models import Answer
from web.player_activities import PlayerActivity
from web.processors import instance_processor as ip

@login_required
def fetch(request, slug):
    # Mission detail
    try:
        mission = Mission.objects.get(slug=slug)
    except:
        raise Http404

    finished_activities = Answer.objects.filter(answerUser=request.user)
    activities = []
    
    for fa in finished_activities:
        activities.append(fa.activity)
    
    tmpl = loader.get_template('missions/base.html')
    return HttpResponse(tmpl.render(RequestContext(request, {
        'mission': mission,
        'activities': activities,
        'comment_form': CommentForm(),
        'active': mission.is_active(),
    }, [ip])))

@login_required
def all(request):
    finished_activities = Answer.objects.filter(answerUser=request.user)
    activities = []
    
    for fa in finished_activities:
        activities.append(fa.activity)

    tmpl = loader.get_template('missions/all.html')
    return HttpResponse(tmpl.render(RequestContext(request, {
        'played': activities,
    }, [ip])))
