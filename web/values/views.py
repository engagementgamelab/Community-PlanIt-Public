import datetime
from operator import itemgetter
import re

from stream import utils as stream_utils

from django.core.urlresolvers import reverse
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils.translation import get_language
from django.shortcuts import get_object_or_404, render_to_response
from django.template import Context, RequestContext, loader

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from web.accounts.models import UserProfile
from web.attachments.models import Attachment
from web.comments.forms import CommentForm
from web.comments.models import Comment
#from reports.models import ActivityLogger
from web.reports.actions import PointsAssigner
from web.values.models import *
from web.core.utils import missions_bar_context

from PIL import Image

@login_required
def all(request, template='values/all.html'):
    if hasattr(request, 'current_game'):
        current_instance = request.current_game
    else:
        raise Http404("could not locate a valid game")
    
    values = Value.objects.untranslated().filter(instance=current_instance)
    community_spent = values.aggregate(Sum('coins'))['coins__sum'] or 0
    
    value_wrapper = []
    player_values = PlayerValue.objects.filter(user=request.user)
    player_spent = player_values.aggregate(Sum('coins'))['coins__sum'] or 0

    for value in values:
        player_value = player_values.filter(value=value)
        coins = float(value.coins)
        if len(player_value) > 0:
            value_wrapper.append({ 'message': value.message, 'value': value, 'coins': coins, 'player_coins': player_value[0].coins, 
                                  'percent': 0 if community_spent == 0 else (coins/community_spent)*100 })
        else:
            value_wrapper.append({ 'message': value.message, 'value': value, 'coins': coins, 'player_coins': 0,
                                   'percent': 0 if community_spent == 0 else (coins/community_spent)*100 })    
    value_wrapper = sorted(value_wrapper, key=itemgetter('message'))

    context = dict(
        values = values,
        value_wrapper = value_wrapper,
        community_spent = community_spent,
        player_spent = player_spent,
    )
    # this line here updates the context with 
    # mission, my_points_for_mission and progress_percentage
    context.update(missions_bar_context(request))

    return render_to_response(template, (RequestContext(request, context)))

@login_required
def detail(request, id):
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

    tmpl = loader.get_template('values/base.html')
    return HttpResponse(tmpl.render(RequestContext(request, {
        'value': value,
        'total_coins': total_coins,
        'comments': value,
        'comment_form': CommentForm(),
    }, 
    #[ip]
    )))

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
        
        #log_url = reverse('values:detail', args=[id])
        #ActivityLogger().log(request.user, request, 'on value: ' + value.message[:30], 'spent token', log_url, 'value')
        stream_utils.action.send(request.user, 'token_spent', action_object=value, description="token spent")
    else:
        messages.error(request, 'No tokens available to spend')
    
    return HttpResponseRedirect(reverse('values:index'))

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
