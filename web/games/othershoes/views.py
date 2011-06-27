import re
import web 
import Image

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.template import RequestContext, loader

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from web.attachments.models import Attachment
from web.comments.forms import CommentForm
from web.comments.models import Comment
from web.games.models import Game, PlayerGame
from web.games.othershoes.models import OtherShoes
from web.missions.models import Mission
from web.processors import instance_processor as ip
from web.reports.actions import PointsAssigner, ActivityLogger
from web.responses.comment.models import CommentResponse
import settings


@login_required
def index(request, mission_slug, id):
    instance = request.user.get_profile().instance
    mission = Mission.objects.get(slug=mission_slug)
    game = get_object_or_404(Game, id=id)
    othershoes = game.othershoes

    if instance.is_expired() or mission.is_expired():
        return HttpResponseRedirect('/mission/'+ mission_slug +'/game/othershoes/'+ id +'/overview/')

    player_game = None
 
    if request.method == 'POST':
        comment_form = CommentForm(request.POST, just_one_form=True)
        if comment_form.is_valid():
            comment = othershoes.comments.create(
                message=comment_form.cleaned_data['message'], 
                user=request.user,
                instance=instance,
            )

            try:
                player_game = PlayerGame.objects.get(user=request.user, game=game)
            except:
                response = CommentResponse(answer=True)
                response.message = comment_form.cleaned_data['message']
                response.save()
                player_game = PlayerGame(visible=True, completed=True, response=response, game=othershoes, user=request.user)
                player_game.save()
                log_url = reverse('games_othershoes_overview', args=[mission_slug, id]) + '#comment-' + str(comment.pk)
                ActivityLogger.log(request.user, request, 'an Other Shoes game', 'completed', log_url, 'othershoes')
                PointsAssigner.assign(request.user, 'othershoes_completed')

                request.session['justplayed'] = True

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

            return HttpResponseRedirect(request.path +'overview')
    else:
        comment_form = CommentForm(just_one_form=True)
    
    fileList = []
    for x in othershoes.prompt.attachments.all():
        fileName = "%s%s" % (settings.MEDIA_ROOT, x.file)
        #Manipulate this to get the image down to a 2:3aspect ratio so
        #200:300
        img = Image.open(fileName)
        x1 = img.size[0]
        y1 = img.size[1]
        fileList.append((x.file, x1, y1))

    tmpl = loader.get_template('games/othershoes/index.html')
    return HttpResponse(tmpl.render(RequestContext(request, {
        'mission': mission,
        'game': game,
        'othershoes': othershoes,
        'comment_form': comment_form,
        'player_game': player_game,
        'fileList': fileList, 
    }, [ip])))

@login_required
def overview(request, mission_slug, id):
    mission = Mission.objects.get(slug=mission_slug)
    game = get_object_or_404(Game, id=id)
    othershoes = game.othershoes
    first_time = request.session.get('justplayed') or False
    request.session['justplayed'] = False

    #if not othershoes.playergame_set.filter(user=request.user).count():
    #    messages.success(request, "You'll have to complete this activity to join its discussion.", extra_tags='sticky')
    #    return HttpResponseRedirect(reverse('games_othershoes_index', args=[mission_slug, id]))

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = othershoes.comments.create(
                message=comment_form.cleaned_data['message'], 
                user=request.user,
                instance=instance,
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
            log_url = reverse('games_othershoes_overview', args=[mission_slug, id]) + '#comment-' + str(comment.pk)
            ActivityLogger.log(request.user, request, 'to Other Shoes response', 'added comment', log_url, 'othershoes')

            return HttpResponseRedirect(request.path +'overview')
    else:
        comment_form = CommentForm()

    other_responses = PlayerGame.objects.all().filter(game=othershoes, completed=True)

    completed_games = PlayerGame.objects.filter(user=request.user, completed=True)
    unplayed = mission.games.exclude(pk=game.pk).exclude(playergame__in=completed_games)
    unplayed = unplayed.count() and unplayed[0] or None
    
    tmpl = loader.get_template('games/othershoes/overview.html')
    return HttpResponse(tmpl.render(RequestContext(request, {
        'mission': mission,
        'game': game,
        'othershoes': othershoes,
        'unplayed': unplayed,
        'first_time': first_time,
        'other_responses': other_responses[:5]
    }, [ip])))

@login_required
def response(request, mission_slug, id, user_id):
    mission = Mission.objects.get(slug=mission_slug)
    game = Game.objects.get(id=id)
    othershoes = game.othershoes
    user = User.objects.get(id=user_id)

    player_game = PlayerGame.objects.get(user=user, game=game)

    other_responses = PlayerGame.objects.all().filter(game=othershoes, completed=True)

    tmpl = loader.get_template('games/othershoes/response.html')
    return HttpResponse(tmpl.render(RequestContext(request, {
        'other_responses': other_responses[:5],
        'mission': mission,
        'game': game,
        'othershoes': othershoes,
        'user': user,
        'player_game': player_game,
        'comments': player_game,
        'response': player_game.response,
        'comment_form': CommentForm(),
    }, [ip])))

