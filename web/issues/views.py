import datetime, re
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import Context, RequestContext, loader
from web.accounts.models import UserProfile
from web.issues.models import *
from web.comments.models import Comment
from web.attachments.models import Attachment
from web.comments.forms import CommentForm
from web.reports.actions import ActivityLogger, PointsAssigner
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from web.processors import instance_processor as ip

@login_required
def fetch(request, id):
    players = UserProfile.objects.all()
    issues = Issue.objects.filter(instance=request.user.get_profile().instance)
    issue = Issue.objects.get(id=id)

    total_coins = 0
    
    for player in players:
        total_coins += player.coins

    tmpl = loader.get_template('issues/base.html')
    return HttpResponse(tmpl.render(RequestContext(request, {
        'issue': issue,
        'total_coins': total_coins,
        'comments': issue,
        'comment_form': CommentForm(),
    }, [ip])))

@login_required
def comment(request, id):
    a = None
    b = None

    if request.method == 'POST':
        if request.POST.has_key('yt-url'):
            if request.POST.get('yt-url'):
                url = re.search(r"(?<=v=)[a-zA-Z0-9-]+(?=&)|(?<=[0-9]/)[^&\n]+|(?<=v=)[^&\n]+", request.POST.get('yt-url')).group()

                if len(url) > 1:
                    a = Attachment(
                        file=None,
                        url=url,
                        type='video',
                        user=request.user,
                        instance=request.user.get_profile().instance,
                    )
                    a.save()
        
        if request.FILES.has_key('picture'):
            b = Attachment(
                file=request.FILES.get('picture'),
                user=request.user,
                instance=request.user.get_profile().instance,
            )

            b.save()

        form = CommentForm(request.POST)
        if form.is_valid():
            c = Comment(
                message=form.cleaned_data['message'], 
                user=request.user,
                instance=request.user.get_profile().instance,
            )
            c.save()

            if a:
                c.attachment.add(a)
                c.save()

            if b:
                c.attachment.add(b)
                c.save()

            issue = Issue.objects.get(id=id)
            issue.comments.add(c)
            issue.save()
            PointsAssigner.assign(request.user, 'comment_created')
            ActivityLogger.log(request.user, request, 'to issue', 'added comment', '/issue/'+ id, 'issue')
        else:
            return HttpResponseRedirect('/issue/'+ id +'?error=true')

    return HttpResponseRedirect('/issue/'+ id)

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
            total_playerCoins = player_issue[0].coins
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
def spend(request, id):
    user = request.user
    profile = user.get_profile()
    issue = Issue.objects.get(id=id)

    playerissue, created = PlayerIssue.objects.get_or_create(user=user, issue=issue)

    if profile.coins > 0:
        issue.coins += 1
        playerissue.coins += 1
        profile.coins -= 1
    
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
        profile.coins += 1
    
        issue.save()
        playerissue.save()
        profile.save()
    
        ActivityLogger.log(request.user, request, 'on issue', 'reclaimed coin', '/issue/'+ str(issue.id), 'issue')
    else:
        messages.info(request, 'No coins available to take')
        
    return HttpResponseRedirect("/issue")
