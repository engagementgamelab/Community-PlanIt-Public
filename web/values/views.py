import datetime
import re

from django.core.urlresolvers import reverse
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.template import Context, RequestContext, loader

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from web.accounts.models import UserProfile
from web.attachments.models import Attachment
from web.comments.forms import CommentForm
from web.comments.models import Comment
from web.processors import instance_processor as ip
from web.reports.actions import ActivityLogger, PointsAssigner
from web.values.models import *

@login_required
def all(request):
    values = Value.objects.filter(instance=request.user.get_profile().instance)
    community_spent = values.aggregate(Sum('coins'))['coins__sum'] or 0
    
    value_wrapper = []
    player_values = PlayerValue.objects.filter(user=request.user)
    
    player_spent = player_values.aggregate(Sum('coins'))['coins__sum'] or 0

    for value in values:
        player_value = player_values.filter(value=value)
        coins = float(value.coins)
        if len(player_value) > 0:
            value_wrapper.append({ 'value': value, 'coins': coins, 'player_coins': player_value[0].coins, 
                                  'percent': 0 if community_spent == 0 else (coins/community_spent)*100 })
        else:
            value_wrapper.append({ 'value': value, 'coins': coins, 'player_coins': 0,
                                   'percent': 0 if community_spent == 0 else (coins/community_spent)*100 })    

    tmpl = loader.get_template('values/all.html')
    return HttpResponse(tmpl.render(RequestContext(request, {
        'values': values,
        'value_wrapper': value_wrapper,
        'community_spent' : community_spent,
        'player_spent' : player_spent,
    }, [ip])))

@login_required
def detail(request, id):
    value = get_object_or_404(Value, id=id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = value.comments.create(
                message=form.cleaned_data['message'], 
                user=request.user,
                instance=request.user.get_profile().instance,
            )

            if request.POST.has_key('yt-url'):
                url = request.POST.get('yt-url')
                if url:
                    comment.attachment.create(
                        file=None,
                        url=url,
                        type='video',
                        user=request.user,
                        instance=request.user.get_profile().instance,
                    )
            
            if request.FILES.has_key('picture'):
                comment.attachment.create(
                    file=request.FILES.get('picture'),
                    user=request.user,
                    instance=request.user.get_profile().instance,
                )

            PointsAssigner.assign(request.user, 'comment_created')
            log_url = reverse('values_detail', args=[id]) + '#comment-' + str(comment.pk)
            ActivityLogger.log(request.user, request, 'to value', 'added comment', log_url, 'value')
            return HttpResponseRedirect(reverse('values_detail', args=[id]))

    values = Value.objects.filter(instance=request.user.get_profile().instance)
    total_coins = values.aggregate(Sum('coins'))['coins__sum'] or 0

    tmpl = loader.get_template('values/base.html')
    return HttpResponse(tmpl.render(RequestContext(request, {
        'value': value,
        'total_coins': total_coins,
        'comments': value,
        'comment_form': CommentForm(),
    }, [ip])))

@login_required
def spend(request, id):
    user = request.user
    profile = user.get_profile()
    value = Value.objects.get(id=id)

    playervalue, created = PlayerValue.objects.get_or_create(user=user, value=value)
    if profile.currentCoins > 0:
        value.coins += 1
        playervalue.coins += 1
        profile.currentCoins -= 1
    
        value.save()
        playervalue.save()
        profile.save()
        
        log_url = reverse('values_detail', args=[id])
        ActivityLogger.log(request.user, request, 'on value', 'spent token', log_url, 'value')
    else:
        messages.info(request, 'No coins available to spend')
    
    return HttpResponseRedirect(reverse('values'))

@login_required
def take(request, id):
    user = request.user
    profile = user.get_profile()
    value = Value.objects.get(id=id)

    playervalue, created = PlayerValue.objects.get_or_create(user=user, value=value)

    if playervalue.coins > 0:
        value.coins -= 1
        playervalue.coins -= 1
        profile.currentCoins += 1
    
        value.save()
        playervalue.save()
        profile.save()
    
        log_url = reverse('values_detail', args=[id])
        ActivityLogger.log(request.user, request, 'on value', 'reclaimed token', log_url, 'value')
    else:
        messages.info(request, 'No coins available to take')
        
    return HttpResponseRedirect(reverse('values'))
