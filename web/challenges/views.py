import re, datetime
from web.challenges.models import *
from web.challenges.forms import *
from web.comments.models import Comment
from web.comments.forms import CommentForm
from web.responses.comment.forms import CommentAttachmentResponseForm
from web.reports.actions import ActivityLogger, PointsAssigner
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import Context, RequestContext, loader
from django.contrib.auth.decorators import login_required
from web.processors import instance_processor as ip

@login_required
def fetch(request, id):
    try:
        challenge = Challenge.objects.get(id=id)
    except:
        raise Http404
    
    playerchallenge = PlayerChallenge.objects.filter(player=request.user, challenge=challenge,accepted=True)
    playerchallenge_completed = PlayerChallenge.objects.filter(player=request.user, challenge=challenge,completed=True)
    playerchallenge_accepted = PlayerChallenge.objects.filter(player=request.user, challenge=challenge,accepted=True).exclude(completed=True)
    
    completed = False
    try:
        pc = PlayerChallenge.objects.filter(player=request.user, challenge=challenge, completed=True)
        if len(pc) > 0:
            completed = True
    except:
        pass

    if playerchallenge_accepted:
        pc = PlayerChallenge.objects.get(player=request.user, challenge=challenge, accepted=True)
        carf = CommentAttachmentResponseForm(instance=pc.response)
    else:
        carf = None

    pc_all = PlayerChallenge.objects.filter(challenge=challenge, completed=True)

    tmpl = loader.get_template('challenges/base.html')
    return HttpResponse(tmpl.render(RequestContext(request, {
        'challenge': challenge,
        'comments': challenge,
        'playerchallenge': playerchallenge,
        'playerchallenge_completed': playerchallenge_completed,
        'playerchallenge_accepted': playerchallenge_accepted,
        'playerchallenge_all': pc_all,
        'comment_form': CommentForm(),
        'completed': completed,
        'response_form': carf,
    },[ip])))

@login_required
def complete(request, id):
    challenge = Challenge.objects.get(id=id)
    pc = PlayerChallenge.objects.get(player=request.user, challenge=challenge)

    a = None
    b = None

    if request.method == 'POST':
        if not pc.completed:
            carf = CommentAttachmentResponseForm(request.POST)

            if request.POST.has_key('yt-url'):
                if request.POST.get('yt-url'):
                    a = Attachment(
                        file=None,
                        url=request.POST.get('yt-url'),
                        type='video',
                        user=request.user,
                        instance=request.user.get_profile().instance
                    )

                    a.save()
            
            if request.FILES.has_key('picture'):
                b = Attachment(
                    file=request.FILES.get('picture'),
                    user=request.user,
                    instance=request.user.get_profile().instance
                )

                b.save()

            ActivityLogger.log(request.user, request, 'a challenge', 'completed', '/challenge/'+ id, 'challenge')
            PointsAssigner.assign(request.user, 'challenge_completed')

            if a:
                pc.attachments.add(a)
                pc.save()

            if b:
                pc.attachments.add(b)
                pc.save()

            if carf.is_valid():
                pc.response = carf.save()
            
            pc.completed = True
            pc.save()

    return HttpResponseRedirect('/challenge/'+ id)

@login_required
def accept(request, id):
    challenge = Challenge.objects.get(id=id)
    pc, created = PlayerChallenge.objects.get_or_create(player=request.user, challenge=challenge)
    ActivityLogger.log(request.user, request, 'a challenge', 'accepted', '/challenge/'+ id, 'challenge')

    pc.accepted = True
    pc.save()

    return HttpResponseRedirect('/challenge/'+ id)

@login_required
def decline(request, id):
    try:
        pc, created = PlayerChallenge.objects.get_or_create(player=request.user, challenge__id=id)
        ActivityLogger.log(request.user, request, 'challenge', 'declined', '/challenge/'+ id, 'challenge')
    except:
        challenge = Challenge.objects.get(id=id)
        pc = PlayerChallenge(player=request.user, challenge=challenge)

    pc.accepted = False
    pc.save()
        
    return HttpResponseRedirect('/challenge')

@login_required
def add(request):
    instance = request.user.get_profile().instance

    if request.method == 'POST':
        form = AddChallenge(request.POST)
        if form.is_valid():
            map = None
            if (request.POST.get('map', None) == None or request.POST.get('map', None) == "None"):
                map = instance.location
            else:
                map = form.cleaned_data['map']

            challenge = Challenge(
                map = map,
                name = form.cleaned_data['name'],
                description = form.cleaned_data['description'],
                start_date = form.cleaned_data['start_date'],
                end_date = form.cleaned_data['end_date'],

                instance = instance,
                user = request.user,
            )
            challenge.save()

            PointsAssigner.assign(request.user, 'challenge_created')
            ActivityLogger.log(request.user, request, 'a challenge', 'created', '/challenge/'+ str(challenge.id), 'challenge')

            return HttpResponseRedirect('/challenge')
    else:
        form = AddChallenge()

    location = instance.location
    
    tmpl = loader.get_template('challenges/add.html')
    return HttpResponse(tmpl.render(RequestContext(request, {
        'instance': instance,
        'form': form,
        'location': location.coordinates,
    },[ip])))

@login_required
def delete(request, id):
    try:
        pc = PlayerChallenge.objects.get(challenge__id=id)
        pc.delete()

        challenge = Challenge.objects.get(id=id)
        challenge.delete()

        ActivityLogger.log(request.user, request, 'challenge', 'deleted', 'challenge')
    except:
        pass

    return HttpResponseRedirect('/challenge')

@login_required
def update(request):
    pass

@login_required
def comment(request, id):
    a = None
    b = None
    instance = request.user.get_profile().instance

    if request.method == 'POST':
        if request.POST.has_key('yt-url'):
            url = request.POST.get('yt-url')
            if url:
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
                instance=instance,
            )
            c.save()

            if a:
                c.attachment.add(a)
                c.save()

            if b:
                c.attachment.add(b)
                c.save()

            challenge = Challenge.objects.get(id=id)
            challenge.comments.add(c)
            challenge.save()

            PointsAssigner.assign(request.user, 'comment_created')
            ActivityLogger.log(request.user, request, 'to challenge', 'added comment', '/challenge/'+ id, 'challenge')
        else:
            return HttpResponseRedirect('/challenge/'+ id +'?error=true')

    return HttpResponseRedirect('/challenge/'+ id)

@login_required
def all(request):
    instance = request.user.get_profile().instance

    player_challenges = PlayerChallenge.objects.filter(player=request.user).filter(challenge__start_date__lt=datetime.datetime.now()).filter(challenge__end_date__gt=datetime.datetime.now()).order_by('challenge__end_date')
    challenges = Challenge.objects.filter(instance=instance).order_by('end_date')
    past_challenges = Challenge.objects.filter(instance=instance).filter(end_date__lt=datetime.datetime.now()).order_by('start_date')
    new_challenges = Challenge.objects.filter(instance=instance).filter(end_date__gt=datetime.datetime.now()).order_by('start_date')
    completed_challenges = []
    current_challenges = []
    
    post = ""
    for x in new_challenges:
        post = "%snew_challenges: %s<br>" % (post, x.id)
    for x in challenges:
        post = "%schallenges: %s<br>" % (post, x.id)
    #return HttpResponse(post)

    
    for player_challenge in player_challenges:
        challenges = challenges.exclude(id=player_challenge.challenge.id)
        new_challenges = new_challenges.exclude(id=player_challenge.challenge.id)
        
        if player_challenge.completed:
            completed_challenges.append(player_challenge)

        if player_challenge.accepted:
            if not player_challenge.completed:
                current_challenges.append(player_challenge)

    tmpl = loader.get_template('challenges/all.html')

    return HttpResponse(tmpl.render(RequestContext(request, {
        'instance': instance,
        'past_challenges': past_challenges,
        'player_challenges': player_challenges,
        'challenges': challenges,
        'new_challenges': new_challenges,
        'completed_challenges': completed_challenges,
        'current_challenges': current_challenges,
    }, [ip])))
