import datetime
#from operator import itemgetter
import simplejson
#import re

from PIL import Image
from sijax import Sijax

from stream import utils as stream_utils

from django.core.urlresolvers import reverse
from django.db.models import Sum
from django.core.cache import cache
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.template import Context, RequestContext, loader

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.datastructures import SortedDict

from web.accounts.models import UserProfile, UserProfilePerInstance
from web.comments.forms import CommentForm
from web.comments.utils import create_video_attachment, create_image_attachment
#from reports.models import ActivityLogger

from web.core.utils import missions_bar_context
from .models import *

import logging
log = logging.getLogger(__name__)


@login_required
def all(request, template='values/all.html'):
    if hasattr(request, 'current_game'):
        current_instance = request.current_game
    else:
        raise Http404("could not locate a valid game")
    values_sorted = SortedDict()
    for v in Value.objects.filter(instance=current_instance).order_by('pk'):
        values_sorted[v] = dict(
                community_spent_total = PlayerValue.objects.filter(value=v).aggregate(Sum('coins'))['coins__sum'] or 0,
                individual_spent_total = PlayerValue.objects.filter(value=v, user=request.user).aggregate(Sum('coins'))['coins__sum'] or 0,
        )

    log.debug(values_sorted)

    context = dict(
        values_sorted = values_sorted,
    )
    # this line here updates the context with 
    # mission, my_points_for_mission and progress_percentage
    context.update(missions_bar_context(request))

    return render(request, template, context)


@login_required
def spend(request):

    if hasattr(request, 'current_game'):
        current_instance = request.current_game
    else:
        raise Http404("could not locate a valid game")

    try:
        prof_per_instance = UserProfilePerInstance.objects.get(
                    instance=request.current_game, 
                    user_profile=request.user.get_profile()
        )
        
    except UserProfilePerInstance.DoesNotExist:
        raise Http404("user for this game is not registered")

    values = list(Value.objects.filter(instance=current_instance).order_by('pk'))
    
    flags_spent=simplejson.loads(request.raw_post_data) # ie. [0, 2, 0, 0, 1]
    
    if sum(flags_spent) > prof_per_instance.flags:
        raise Exception("User does not have enough flags accumulated to spend.")
    
    if len(values) != len(flags_spent):
        raise Exception("Mismatch of values to flags spent in map the future form")
    
    for i in range(len(values)):
        log.debug("v: %s, spent %s" % (values[i], flags_spent[i]))
    
        playervalue, created = PlayerValue.objects.get_or_create(user=request.user, value=values[i])
        if created:
            playervalue.coins = flags_spent[i]
        else:
            playervalue.coins+=flags_spent[i]
    
        playervalue.save()
    
        log.debug("%s spent %s flags on %s" % (request.user.get_profile().screen_name, flags_spent[i], values[i].__unicode__()))
    
        stream_utils.action.send(
                    request.user,
                    'flag_spent',
                    action_object=values[i], description="planted a flag on the priority",
                    target=current_instance
        )
        cache.invalidate_group('my_spent_flags')
    
    return redirect(reverse('values:index'))

@login_required
def detail(request, id, template='values/value.html'):
    value = get_object_or_404(Value, id=id)

    if hasattr(request, 'current_game'):
        current_instance = request.current_game
    else:
        raise Http404("could not locate a valid game")

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = value.comments.create(
                    content_object=value,
                    message=form.cleaned_data['message'], 
                    user=request.user,
                    instance=value.instance
            )
            if request.POST.has_key('video-url') and request.POST.get('video-url') != '':
                create_video_attachment(comment, request.POST.get('video-url'), request.current_game, request.user)

            if request.FILES.has_key('picture'):
                create_image_attachment(comment, request.FILES.get('picture'), request.current_game, request.user)

            return redirect(value.get_absolute_url())

    total_flags_by_game = PlayerValue.objects.total_flags_by_game(current_instance, value)
    my_total_flags_for_value = PlayerValue.objects.total_flags_for_player(current_instance, request.user, value=value)

    context = {
        'value': value,
        'total_flags_by_game': total_flags_by_game,
        'my_total_flags_for_value': my_total_flags_for_value,
        'comments': value,
        'comment_form': CommentForm(),
    }
    context.update(missions_bar_context(request))
    return render(request, template, context)

@login_required
def take(request, id):
    user = request.user
    profile = user.get_profile()
    try:
        value = Value.objects.get(id=id)
    except Value.DoesNotExist:
        return Http404("Value with id %s does not exist" % id)

    playervalue, created = PlayerValue.objects.get_or_create(user=user, value=value)

    if playervalue.coins > 0:
        value.coins -= 1
        playervalue.coins -= 1
        profile.currentCoins += 1
    
        value.save()
        playervalue.save()
        profile.save()
    
        #log_url = reverse('values:detail', args=[id])
        #ActivityLogger().log(request.user, request, 'from value: ' + value.message[:30], 'reclaimed token', log_url, 'value')
        stream_utils.action.send(request.user, 'token_reclaimed', action_object=value, description="token reclaimed")
    else:
        messages.info(request, 'No coins available to take')
        
    return redirect(reverse('values:index'))
