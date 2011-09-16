import datetime
from operator import attrgetter

from django.db.models import Q
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.translation import get_language

from django.contrib.auth.decorators import login_required

from answers.models import *
from comments.forms import CommentForm
from comments.models import Comment
from instances.models import Instance
from missions.models import *
from player_activities.models import *

@login_required
def fetch(request, slug, template='missions/base.html'):
    if request.user.is_superuser:
        my_instance = Instance.objects.all()[0]
    else:
        my_profile = request.user.get_profile()
        my_instance = my_profile.instance
    mission = get_object_or_404(Mission, slug=slug, instance=my_instance)

    activities = []
    for model_klass in [PlayerActivity, PlayerEmpathyActivity, PlayerMapActivity]:
        activities.extend(list(model_klass.objects.filter(mission=mission)))
    activities = sorted(activities, key=attrgetter('name'))

    completed = []
    for activity in activities:
        if activity.is_completed(request.user):
            completed.append(activity)

    context = dict(
        mission = mission,
        activities = activities,
        completed = completed,
        comment_form = CommentForm(),
    )
    return render_to_response(template, RequestContext(request, context))
    
@login_required
def all(request, template="missions/all.html"):
    #TODO
    #finished_activities = PlayerActivity.objects.filter(answers__answerUser=request.user)

    #TODO
    # for now show admins just pick the first instance
    if request.user.is_superuser:
        my_instance = Instance.objects.all()[0]
    else:
        my_profile = request.user.get_profile()
        my_instance = my_profile.instance
    context = dict(
            active_missions = my_instance.missions.active(),
            future_missions = my_instance.missions.future(),
            past_missions = my_instance.missions.past(),
            #played = finished_activities,
    )
    return render_to_response(template, RequestContext(request, context))
