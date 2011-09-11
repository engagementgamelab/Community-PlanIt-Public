import datetime

from django.db.models import Q
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.translation import get_language

from django.contrib.auth.decorators import login_required

from comments.forms import CommentForm
from comments.models import Comment
from instances.models import Instance
from missions.models import *
from player_activities.models import *
from answers.models import *

@login_required
def fetch(request, slug, template='missions/base.html'):
    mission = get_object_or_404(Mission, slug=slug, instance=request.user.get_profile().instance)

    activities = []
    completed = []

    for model_klass in [PlayerActivity, PlayerEmpathyActivity, PlayerMapActivity]:
        activities.extend(
                list(model_klass.objects.language(get_language()).filter(mission=mission))
        )

    for activity in activities:
        for answer_klass in [AnswerEmpathy, AnswerMap, AnswerSingleResponse]:
            related_name = answer_klass.__name__.replace('Answer', '').lower() + '_answers'
            if hasattr(activity, related_name) and getattr(activity, related_name).all():
                completed.append(activity)

        #if activity.type.type == 'multi_reponse':
        #    answers = AnswerMultiChoice.objects.filter(user=request.user, option__activity__mission=mission)
        #    print answers

            #TODO
        #isAnswerMultiChoice]
        #for mc in AnswerMultiChoice.objects.filter(user=request.user, option__activity__mission=mission):
        #    pk = mc.option.activity.pk
        #    if pk not in pks:
        #        pks.append(pk)

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

    my_profile = request.user.get_profile()
    my_instance = my_profile.instance
    context = dict(
            active_missions = my_instance.missions.active(),
            future_missions = my_instance.missions.future(),
            past_missions = my_instance.missions.past(),
            #played = finished_activities,
    )
    return render_to_response(template, RequestContext(request, context))
