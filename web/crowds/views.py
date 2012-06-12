import datetime
import re
from stream import utils as stream_utils
from PIL import Image

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render_to_response, render
from django.template import Context, RequestContext, loader

from django.contrib.auth.decorators import login_required

from web.core.utils import missions_bar_context
from web.comments.forms import CommentForm
from web.comments.models import Comment
from web.reports.actions import PointsAssigner
#from responses.comment.forms import CommentAttachmentResponseForm
from .forms import *
from .models import *

import logging
log = logging.getLogger(__name__)

@login_required
def view_crowd(request, id, template='crowds/crowd.html'):

    if hasattr(request, 'current_game'):
        current_instance = request.current_game
    else:
        raise Http404("could not locate a valid game")

    # if current_instance.is_expired():
    #     return HttpResponseRedirect(reverse('crowds:index'))

    crowd = Crowd.objects.get(id=id)
    
    context = {
        'crowd': crowd,
    }
    context.update(missions_bar_context(request))
    return render(request, template, context)

@login_required
def join_crowd(request, id):

    if hasattr(request, 'current_game'):
        current_instance = request.current_game
    else:
        raise Http404("could not locate a valid game")

    # if current_instance.is_expired():
    #     return HttpResponseRedirect(reverse('crowds:index'))

    crowd = Crowd.objects.get(id=id)
    crowd.participants.add(request.user)

    #stream_utils.action.send(request.user, 'crowd_joined', target=current_instance, action_object=crowd, 
    #                        description="A challenge was accepted"
    #)
    return HttpResponseRedirect(reverse('crowds:view', args=[id]))

@login_required
def leave_crowd(request, id):

    if hasattr(request, 'current_game'):
        current_instance = request.current_game
    else:
        raise Http404("could not locate a valid game")


    # if current_instance.is_expired():
    #     return HttpResponseRedirect(reverse('crowds:index'))

    crowd = Crowd.objects.get(id=id)
    crowd.participants.remove(request.user)

    #stream_utils.action.send(request.user, 'crowd_joined', target=current_instance, action_object=crowd, 
    #                        description="A challenge was accepted"
    #)
    return HttpResponseRedirect(reverse('crowds:view', args=[id]))



@login_required
def create(request):

    if hasattr(request, 'current_game'):
        current_instance = request.current_game
    else:
        raise Http404("could not locate a valid game")

    # if current_instance.is_expired():
    #     return HttpResponseRedirect(reverse('crowds:index'))

    if request.method == 'POST':
        form = CrowdForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            # TODO include the address on the CrowdForm
            address = request.POST.get("google_search")
            log.debug("new crowd address --> %s" % address)
            log.debug("create crowd cleaned data: %s" % cd)
            map = None
            if (cd.get('map', None) == None or cd.get('map', None) == "None"):
                map = current_instance.location
            else:
                map = cd['map']

            crowd = form.save(commit=False)
            crowd.map = map
            # TODO how is the size supposed to be set?
            # the map will not render if the size is missing.
            crowd.map.size = [500, 400]
            crowd.address = address
            crowd.instance = current_instance
            crowd.creator = request.user
            crowd.save()
            crowd.participants.add(request.user)
            #gno PointsAssigner().assign(request.user, 'challenge_created')
            #ActivityLogger().log(request.user, request, 'a challenge: ' + challenge.name[:30], 'created', reverse('challenges:challenge', args=[challenge.id]), 'challenge')
            #stream_utils.action.send(request.user, 'challenge_created', target=current_instance, action_object=challenge, 
            #                         description="A challenge was created"
            #)
            return HttpResponseRedirect(reverse('crowds:index'))
        else:
            log.debug("create crowd errors: %s" % form.errors)

    else:
        form = CrowdForm()
    context = {
        'map': current_instance.location,
        'upcoming_crowds': Crowd.objects.upcoming().filter(instance=current_instance),
        'past_crowds': Crowd.objects.past().filter(instance=current_instance),
        'form': form,
    }
    
    context.update(missions_bar_context(request))
    return render(request, 'crowds/add.html', context)


@login_required
def update(request):
    pass

@login_required
def comment(request, id):
    a = None
    b = None
    instance = request.user.get_profile().instance
    if instance.is_expired():
        return HttpResponseRedirect(reverse('challenges:index'))

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
            #ActivityLogger().log(request.user, request, 'to a challenge: ' + challenge.name[:30], 'added comment', reverse('challenges:challenge', args=[id]), 'challenge')
            #stream_utils.action.send(request.user, 'challenge_commented', target=challenge, action_object=c, description="Commented on a challenge"
            #)

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
def all(request, template='crowds/all.html', extra_context={}):
    
    if hasattr(request, 'current_game'):
        current_instance = request.current_game
    else:
        raise Http404("could not locate a valid game")
    
    context = {
        'upcoming_crowds': Crowd.objects.upcoming().filter(instance=current_instance),
        'past_crowds': Crowd.objects.past().filter(instance=current_instance),
    }
    
    context.update(extra_context)
    context.update(missions_bar_context(request))
    return render(request, template, context)



