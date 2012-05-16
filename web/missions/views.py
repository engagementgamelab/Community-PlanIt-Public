import datetime
from operator import attrgetter

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.http import Http404

from .models import *
from web.core.utils import missions_bar_context
from web.accounts.models import UserProfilePerInstance

import logging
log = logging.getLogger(__name__)

@login_required
def fetch(request, slug, include_player_submitted=False, template='missions/mission.html'):
    # expecting the current game to be 
    # set by middleware
    if not hasattr(request, 'current_game'):
        raise Http404("could not locate a valid game")

    try:
        prof_per_instance = UserProfilePerInstance.objects.get(
                    instance=request.current_game, 
                    user_profile=request.user.get_profile()
        )
    except UserProfilePerInstance.DoesNotExist:
        raise Http404("user for this game is not registered")

    
    # TODO: Should only return non-player-created challenges
    mission = get_object_or_404(Mission, slug=slug)
    my_completed = set(prof_per_instance.my_completed_by_mission(mission, include_player_submitted))
    #my_completed = set()

    log.debug("%s completed %s challenges" % (prof_per_instance, len(my_completed)))
    
    my_incomplete = set(
                            Mission.objects.activities_for_mission(
                                        mission.slug, 
                                        include_player_submitted
                            ) 
                        ) - my_completed
    my_incomplete = sorted(list(my_incomplete), key=attrgetter('name'))

    my_completed = sorted(list(my_completed), key=attrgetter('name'))

    my_incomplete.extend(my_completed)
    all_activities_sorted = my_incomplete
    
    all_player_submitted = set(Mission.objects.activities_for_mission(mission.slug, True))
    
    #log.debug(all_activities_sorted)
    context = dict(
        all_player_submitted = all_player_submitted,
        activities = all_activities_sorted,
        my_completed = my_completed,
    )
    # this line here updates the context with 
    # mission, my_points_for_mission and progress_percentage
    context.update(missions_bar_context(request, mission))
    return render(request, template, context)
