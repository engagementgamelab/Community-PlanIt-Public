import datetime

#from stream.models import Action

from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.http import Http404

from django.contrib.auth.decorators import login_required

from web.core.utils import missions_bar_context
from web.answers.models import *
from web.comments.forms import CommentForm
from web.comments.models import Comment
from web.instances.models import Instance
from web.missions.models import *
from web.player_activities.models import *

import logging
log = logging.getLogger(__name__)

@login_required
def fetch(request, slug, include_player_submitted=False, template='missions/base.html'):
    # expecting the current game to be 
    # set by middleware
    print 'asdfasdfasdf'
    if not hasattr(request, 'current_game'):
        raise Http404("could not locate a valid game")
    
    # TODO: Should only return non-player-created challenges
    mission = get_object_or_404(Mission, slug=slug)
    my_completed = set(request.prof_per_instance.my_completed_by_mission(mission, include_player_submitted))
    log.debug("i completed %s challenges" % len(my_completed))
    my_not_completed = set(mission.get_activities(include_player_submitted)) - my_completed
    my_not_completed = list(my_not_completed)
    my_completed = list(my_completed)
    my_not_completed.extend(my_completed)
    all_activities_sorted = my_not_completed
    context = dict(
        activities = all_activities_sorted,
        my_completed = my_completed,
        comment_form = CommentForm(),
    )
    # this line here updates the context with 
    # mission, my_points_for_mission and progress_percentage
    context.update(missions_bar_context(request, mission))
    return render(request, template, context)
