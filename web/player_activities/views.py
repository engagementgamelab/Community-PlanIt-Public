from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, RequestContext, loader
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from web.player_activities.models import PlayerActivity
from web.answers.models import Answer
from web.missions.models import Mission
from web.instances.models import Instance

from web.processors import instance_processor as ip

@login_required
def overview(request):
    return HttpResponse("web page not created yet")

@login_required
def getGame(request):
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
