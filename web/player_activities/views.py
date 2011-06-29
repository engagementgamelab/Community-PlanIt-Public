from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import Context, RequestContext, loader
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from web.player_activities.models import PlayerActivity
from web.answers.models import *
from web.missions.models import Mission
from web.instances.models import Instance

from web.processors import instance_processor as ip
from web.player_activities.forms import *
import settings

@login_required
def overview(request, id):
    return HttpResponse("web page not created yet")

@login_required
def get_activity(request, id):
    activity = PlayerActivity.objects.get(id=id)
    tmpl = None
    form = None
    map = None
    if (activity.type.type == "open_ended"):
        tmpl = loader.get_template('player_activities/open_ended.html')
        form = OpenForm()
    elif (activity.type.type == "single_response"):
        tmpl = loader.get_template('player_activities/single_response.html')
        mc = MultiChoiceActivity.objects.filter(activity=activity)
        choices = []
        for x in mc:
            choices.append((x.id, x.value))
        if settings.DEBUG == True and len(choices) == 0:
            choices.append((1, "Test data"))
            choices.append((2, "More test data"))
            choices.append((3, "This is another test"))
        form = MakeSingleForm(choices)
        #form = SingleForm(choices)
    elif (activity.type.type == "map"):
        tmpl = loader.get_template('player_activities/map_response.html')
        form = MapForm()
        map = activity.mission.instance.location 
    elif (activity.type.type == "empathy"):
        tmpl = loader.get_template('player_activities/empathy.html')
        form = EmpathyForm()
    elif (activity.type.type == "multi_reponse"):
        mc = MultiChoiceActivity.objects.filter(activity=activity)
        choices = []
        for x in mc:
            choices.append((x.id, x.value))
        if settings.DEBUG == True and len(choices) == 0:
            choices.append((1, "Test data"))
            choices.append((2, "More test data"))
            choices.append((3, "This is another test"))
        tmpl = loader.get_template('player_activities/multi_response.html')
        form = MakeMultiForm(choices)
    else:
        raise Http404
    
    return HttpResponse(tmpl.render(RequestContext(request, {
        "form": form, 
        "activity": activity,
        "map": map,
        }, [ip])))
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
