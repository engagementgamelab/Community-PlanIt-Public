import datetime
from operator import attrgetter

from django.utils.translation import get_language
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.http import Http404

from .models import *
from web.core.utils import missions_bar_context
from web.accounts.models import UserProfilePerInstance

import logging
log = logging.getLogger(__name__)

@login_required
def fetch(request, slug, player_submitted_only=False, template='missions/mission.html'):

    mission = get_object_or_404(Mission, slug=slug)
    try:
        prof_per_instance = UserProfilePerInstance.objects.get(
                    instance=mission.instance,
                    user_profile=request.user.get_profile()
        )
    except UserProfilePerInstance.DoesNotExist:
        raise Http404("user for this game is not registered")

    
    # TODO: Should only return non-player-created challenges
    player_submitted = set(mission.player_submitted_activities(lang=get_language()))
    all_activities = player_submitted if player_submitted_only == True else \
            set(mission.activities(lang=get_language())) - player_submitted

    my_completed = set(prof_per_instance.my_completed_by_mission(mission, player_submitted_only))
    my_incomplete = all_activities - my_completed
    my_incomplete = sorted(my_incomplete, key=attrgetter('name'))
    my_completed = sorted(list(my_completed), key=attrgetter('name'))

    my_incomplete.extend(my_completed)
    all_activities_sorted = my_incomplete

    context = dict(
        activities = all_activities_sorted,
        my_completed = my_completed,
        all_player_submitted_cnt = len(player_submitted),
    )
    # this line here updates the context with 
    # mission, my_points_for_mission and progress_percentage
    #context.update(missions_bar_context(request, mission))
    return render(request, template, context)
