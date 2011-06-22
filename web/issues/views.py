import datetime
import re

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.template import Context, RequestContext, loader

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from web.accounts.models import UserProfile
from web.attachments.models import Attachment
from web.comments.forms import CommentForm
from web.comments.models import Comment
from web.issues.models import *
from web.processors import instance_processor as ip
from web.reports.actions import ActivityLogger, PointsAssigner

@login_required
def all(request):
    issues = Issue.objects.filter(instance=request.user.get_profile().instance)
    num_issues = len(issues)
    
    total_coins = 0
    total_playerCoins = 0

    issue_wrapper = []
    playerissues = PlayerIssue.objects.filter(user=request.user)

    # Calculate total coins for next iteration to generate percentages
    for issue in issues:
        total_coins += issue.coins

    for issue in issues:
        player_issue = playerissues.filter(issue=issue)
        coins = issue.coins
        if len(player_issue) > 0:
            total_playerCoins += player_issue[0].coins
            # +0.0 coerces to a float for percentages
            issue_wrapper.append({ 'issue': issue, 'coins': coins, 'player_coins': player_issue[0].coins, 
                                  'percent': 0 if total_coins == 0 else ((coins+0.0)/total_coins)*100 })
        else:
            issue_wrapper.append({ 'issue': issue, 'coins': coins, 'player_coins': 0,
                                   'percent': 0 if total_coins == 0 else ((coins+0.0)/total_coins)*100 })    

    tmpl = loader.get_template('issues/all.html')
    return HttpResponse(tmpl.render(RequestContext(request, {
        'issues': issues,
        'issue_wrapper': issue_wrapper,
        'total_coins' : total_coins,
        'total_playerCoins' : total_playerCoins,
    }, [ip])))

@login_required
def detail(request, id):
    issue = get_object_or_404(Issue, id=id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = issue.comments.create(
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
            log_url = reverse('issues_detail', args=[id]) + '#comment-' + str(comment.pk)
            ActivityLogger.log(request.user, request, 'to issue', 'added comment', log_url, 'issue')
            return HttpResponseRedirect(reverse('issues_detail', args=[id]))

    issues = Issue.objects.filter(instance=request.user.get_profile().instance)
    total_coins = 0
    for i in issues:
        total_coins += i.coins

    tmpl = loader.get_template('issues/base.html')
    return HttpResponse(tmpl.render(RequestContext(request, {
        'issue': issue,
        'total_coins': total_coins,
        'comments': issue,
        'comment_form': CommentForm(),
    }, [ip])))

@login_required
def spend(request, id):
    user = request.user
    profile = user.get_profile()
    issue = Issue.objects.get(id=id)

    playerissue, created = PlayerIssue.objects.get_or_create(user=user, issue=issue)
    if profile.currentCoins > 0:
        issue.coins += 1
        playerissue.coins += 1
        profile.currentCoins -= 1
    
        issue.save()
        playerissue.save()
        profile.save()
        
        ActivityLogger.log(request.user, request, 'on issue', 'spent coin', '/issue/'+ str(issue.id), 'issue')
    else:
        messages.info(request, 'No coins available to spend')
    
    return HttpResponseRedirect("/issue")

@login_required
def take(request, id):
    user = request.user
    profile = user.get_profile()
    issue = Issue.objects.get(id=id)

    playerissue, created = PlayerIssue.objects.get_or_create(user=user, issue=issue)

    if playerissue.coins > 0:
        issue.coins -= 1
        playerissue.coins -= 1
        profile.currentCoins += 1
    
        issue.save()
        playerissue.save()
        profile.save()
    
        ActivityLogger.log(request.user, request, 'on issue', 'reclaimed coin', '/issue/'+ str(issue.id), 'issue')
    else:
        messages.info(request, 'No coins available to take')
        
    return HttpResponseRedirect("/issue")
