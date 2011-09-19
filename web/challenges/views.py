import datetime
import re

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.template import Context, RequestContext, loader

from django.contrib.auth.decorators import login_required

from web.challenges.forms import *
from web.challenges.models import *
from web.comments.forms import CommentForm
from web.comments.models import Comment
#from web.processors import instance_processor as ip
from web.reports.actions import ActivityLogger, PointsAssigner
from web.responses.comment.forms import CommentAttachmentResponseForm
from web.core.utils import _fake_latest

from PIL import Image

@login_required
def fetch(request, id):
    challenge = get_object_or_404(Challenge, id=id)

    try:
        pc = PlayerChallenge.objects.get(player=request.user, challenge=challenge)
    except PlayerChallenge.DoesNotExist:
        pc = None

    if request.method == 'POST':
        pc, created = PlayerChallenge.objects.get_or_create(player=request.user, challenge=challenge)
        if not pc.completed:
            carf = CommentAttachmentResponseForm(request.POST, instance=pc.response)
            if carf.is_valid():
                pc.response = carf.save()
                pc.completed = True
                pc.save()

                ActivityLogger().log(request.user, request, 'a challenge: ' + challenge.name, 'completed', reverse('challenges:challenge', args=[id]), 'challenge')
                PointsAssigner().assign(request.user, 'challenge_completed')

                if pc.player != challenge.user:
                    message = "%s completed %s" % (
                        request.user.get_profile().screen_name,
                        challenge.name
                    )
                    challenge.user.notifications.create(content_object=challenge, message=message)

                if request.POST.has_key('video-url'):
                    if request.POST.get('video-url'):
                        pc.attachments.create(
                            file=None,
                            url=request.POST.get('video-url'),
                            type='video',
                            user=request.user,
                            instance=request.user.get_profile().instance
                        )                
                if request.FILES.has_key('picture'):
                    file = request.FILES.get('picture')
                    picture = Image.open(file)
                    if (file.name.rfind(".") -1):
                        file.name = "%s.%s" % (file.name, picture.format.lower())
                    pc.attachments.create(
                        file=request.FILES.get('picture'),
                        user=request.user,
                        instance=request.user.get_profile().instance
                    )

                    return HttpResponseRedirect(reverse('challenges:challenge', args=[id]))
    else:
        carf = CommentAttachmentResponseForm()

    data = {
        'challenge': challenge,
        'player_challenge': pc,
        'instance': challenge.instance,
        'comment_form': CommentForm(),
        'response_form': carf,
    }

    return render_to_response(
        'challenges/base.html',
        data,
        context_instance=RequestContext(request)
    )

@login_required
def accept(request, id):
    challenge = Challenge.objects.get(id=id)
    pc, created = PlayerChallenge.objects.get_or_create(player=request.user, challenge=challenge)
    ActivityLogger.log(request.user, request, 'a challenge: ' + challenge.name, 'accepted', reverse('challenges:challenge', args=[id]), 'challenge')

    pc.completed = False
    pc.accepted = True
    pc.save()

    return HttpResponseRedirect(reverse('challenges:challenge', args=[id]))

@login_required
def decline(request, id):
    challenge = get_object_or_404(Challenge, id=id)

    pc, created = PlayerChallenge.objects.get_or_create(player=request.user, challenge=challenge)
    ActivityLogger.log(request.user, request, 'a challenge: ' + challenge.name, 'declined', reverse('challenges:challenge', args=[id]), 'challenge')
    
    pc.declined = True
    pc.accepted = False
    pc.save()
        
    return HttpResponseRedirect(reverse('challenges:challenge'))

@login_required
def add(request):
    instance = request.user.get_profile().instance

    if request.method == 'POST':
        form = AddChallenge(instance, request.POST)
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

            PointsAssigner().assign(request.user, 'challenge_created')
            ActivityLogger().log(request.user, request, 'a challenge: ' + challenge.name, 'created', reverse('challenges:challenge', args=[challenge.id]), 'challenge')

            return HttpResponseRedirect(reverse('challenges:index'))
    else:
        form = AddChallenge(instance)

    location = instance.location
    
    tmpl = loader.get_template('challenges/add.html')
    return HttpResponse(tmpl.render(RequestContext(request, {
        'instance': instance,
        'form': form,
        'location': location.coordinates,
    },
    #[ip]
    )))

@login_required
def delete(request, id):
    try:
        pc = PlayerChallenge.objects.get(challenge__id=id)
        pc.delete()

        challenge = Challenge.objects.get(id=id)
        challenge.delete()

        ActivityLogger.log(request.user, request, 'a challenge: ' + challenge.name, 'deleted', 'challenge')
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
        if request.POST.has_key('video-url'):
            url = request.POST.get('video-url')
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
            file = request.FILES.get('picture')
            picture = Image.open(file)
            if (file.name.rfind(".") -1):
                file.name = "%s.%s" % (file.name, picture.format.lower())
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

            PointsAssigner().assign(request.user, 'comment_created')
            ActivityLogger().log(request.user, request, 'to a challenge: ' + challenge.name, 'added comment', reverse('challenges:challenge', args=[id]), 'challenge')

            if request.user != challenge.user:
                message = "%s commented on %s" % (
                    request.user.get_profile().screen_name,
                    challenge
                )
                challenge.user.notifications.create(content_object=challenge, message=message)
        else:
            return HttpResponseRedirect(reverse('challenges:challenge', args=[id]) +'?error=true')

    return HttpResponseRedirect(reverse('challenges:challenge', args=[id]))

@login_required
def all(request):
    instance = None

    profile = request.user.get_profile()
    if profile.instance:
        instance = profile.instance
    elif request.user.is_staff or request.user.is_superuser:

        #instance = Instance.objects.active().latest()
        instance = Instance.objects.untranslated().latest()

    new_challenges = instance.challenges.available(request.user)

    tmpl = loader.get_template('challenges/all.html')

    return HttpResponse(tmpl.render(RequestContext(request, {
        'instance': instance,
        'new_challenges': new_challenges,
    }, 
    #[ip]
    )))
