import datetime
#from operator import itemgetter
from collections import OrderedDict
import json
#import re

from PIL import Image

from stream import utils as stream_utils

from django.core.urlresolvers import reverse
from django.db.models import Sum
from django.core.cache import cache
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils.translation import get_language
from django.shortcuts import get_object_or_404, render, redirect
from django.template import Context, RequestContext, loader

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.datastructures import SortedDict

from web.accounts.models import UserProfile
from web.attachments.models import Attachment
from web.comments.forms import CommentForm
from web.comments.models import Comment
#from reports.models import ActivityLogger
from web.reports.actions import PointsAssigner
from web.values.models import *
from web.core.utils import missions_bar_context

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

    values = list(Value.objects.filter(instance=current_instance).order_by('pk'))

    log.debug("querydict: %s " % request.POST.keys()[0])
    flags_spent = json.loads(request.POST.keys()[0], object_pairs_hook=OrderedDict).values()
    log.debug("flags spent from front-end: %s" % flags_spent)
    if len(values) != len(flags_spent):
        raise Exception("mismatch of values to flags spent in map the future form")

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
                    action_object=values[i], description="token spent",
                    target=current_instance
        )
        cache.invalidate_group('my_spent_flags')

    return redirect(reverse('values:index'))

@login_required
def detail(request, id, template='values/value.html'):
    value = get_object_or_404(Value, id=id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = value.comments.create(
                content_object=value,
                message=form.cleaned_data['message'], 
                user=request.user,
                instance=value.instance
            )

            if request.POST.has_key('video-url'):
                url = request.POST.get('video-url')
                if url:
                    comment.attachment.create(
                        file=None,
                        url=url,
                        type='video',
                        user=request.user,
                        instance=value.instance
                    )
            file = request.FILES.get('picture')
            if file:
                picture = Image.open(file)
                if (file.name.rfind(".") -1):
                    file.name = "%s.%s" % (file.name, picture.format.lower())
                if request.FILES.has_key('picture'):
                    comment.attachment.create(
                        file=request.FILES.get('picture'),
                        user=request.user,
                        instance=value.instance
                    )

            PointsAssigner().assign(request.user, 'comment_created')
            log_url = reverse('values:detail', args=[id]) + '#comment-' + str(comment.pk)
            #ActivityLogger().log(request.user, request, 'to value: ' + value.message[:30], 'added comment', log_url, 'value')
            return HttpResponseRedirect(reverse('values:detail', args=[id]))

    values = value.instance.values.language(get_language())
    total_coins = values.aggregate(Sum('coins'))['coins__sum'] or 0

    context = {
        'value': value,
        'total_coins': total_coins,
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
        
    return HttpResponseRedirect(reverse('values:index'))
