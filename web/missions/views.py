import datetime

from django.db.models import Q
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.translation import get_language

from django.contrib.auth.decorators import login_required

from web.answers.models import Answer, AnswerMultiChoice
from web.comments.forms import CommentForm
from web.comments.models import Comment
from web.instances.models import Instance
from web.missions.models import *
from web.player_activities.models import PlayerActivity

@login_required
def fetch(request, slug, template='missions/base.html'):
    mission = get_object_or_404(Mission, slug=slug, instance=request.user.get_profile().instance)

    pks = []
    for pk in Answer.objects.filter(answerUser=request.user, activity__mission=mission):
        pks.append(pk.activity.pk)
    
    for mc in AnswerMultiChoice.objects.filter(user=request.user, option__activity__mission=mission):
        pk = mc.option.activity.pk
        if pk not in pks:
            pks.append(pk)
    activities = PlayerActivity.objects.language(get_language()).filter(mission=mission)
    answered_activities = PlayerActivity.objects.language(get_language()).filter(Q(pk__in=pks))
    unfinished_activities = PlayerActivity.objects.language(get_language()).filter(Q(mission=mission) & ~Q(pk__in=pks))

    #import ipdb;ipdb.set_trace()

    context = dict(
        mission = mission,
        activities = activities,
        unfinished_activities = unfinished_activities,
        answered_activities = answered_activities,
        comment_form = CommentForm(),
    )

    return render_to_response(template, RequestContext(request, context))
    
@login_required
def all(request, template="missions/all.html"):
    finished_activities = PlayerActivity.objects.filter(answers__answerUser=request.user)

    my_profile = request.user.get_profile()
    my_instance = my_profile.instance
    context = dict(
            active_missions = my_instance.missions.active(),
            future_missions = my_instance.missions.future(),
            past_missions = my_instance.missions.past(),
            played = finished_activities,
    )
    return render_to_response(template, RequestContext(request, context))
