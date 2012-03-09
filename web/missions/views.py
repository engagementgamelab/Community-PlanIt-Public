import datetime
from operator import attrgetter

from django.db.models import Q
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

from django.contrib.auth.decorators import login_required

from answers.models import *
from comments.forms import CommentForm
from comments.models import Comment
from instances.models import Instance
from missions.models import *
from player_activities.models import *
from core.utils import instance_from_request

@login_required
def fetch(request, slug, template='missions/base.html'):
    current_instance = instance_from_request(request)
    mission = get_object_or_404(Mission, slug=slug, instance=current_instance)

    activities = []
    for model_klass in [PlayerActivity, PlayerEmpathyActivity, PlayerMapActivity]:
        activities.extend(list(model_klass.objects.filter(mission=mission)))
    activities = sorted(activities, key=attrgetter('name'))

    completed = []
    for activity in activities:
        if activity.is_completed(request.user):
            completed.append(activity)
    
    next_mission = None
    my_missions = Mission.objects.filter(instance=current_instance).exclude(slug=slug).order_by('-start_date')
    if my_missions.count() > 0:
        next_mission = my_missions[0]
        if next_mission.is_expired():
            next_mission = None

    context = dict(
        mission = mission,
        activities = activities,
        completed = completed,
        comment_form = CommentForm(),
        mission_completed = len(activities) == len(completed),
        next_mission = next_mission,
    )
    return render_to_response(template, RequestContext(request, context))
    
@login_required
def all(request, template="missions/all.html", extra_context={}):
    #TODO
    #finished_activities = PlayerActivity.objects.filter(answers__answerUser=request.user)
    # using the mission manager to filter the intances 
    # does not set the context correctly in the template, 
    # {{ current_instance.missions.active  }} does not work.
    # although using it here works fine. go figure nani.
    current_instance = instance_from_request(request)
    context = {"current_instance": "current_instance",
            'active_missions': current_instance.missions.active()}
    if extra_context.keys():
        context.update(extra_context)
    return render_to_response(template, RequestContext(request, context))
