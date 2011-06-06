import re
import web 

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.template import RequestContext, loader

from web.attachments.models import Attachment
from web.comments.forms import CommentForm
from web.comments.models import Comment
from web.games.models import Game, PlayerGame
from web.games.othershoes.models import OtherShoes
from web.missions.models import Mission
from web.processors import instance_processor as ip
from web.reports.actions import PointsAssigner, ActivityLogger
from web.responses.comment.models import CommentResponse

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
                if request.POST.get('yt-url'):
                    url = re.search(r"(?<=v=)[a-zA-Z0-9-]+(?=&)|(?<=[0-9]/)[^&\n]+|(?<=v=)[^&\n]+", request.POST.get('yt-url')).group()

                    if len(url) > 1:
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

    tmpl = loader.get_template('games/othershoes/index.html')
    return HttpResponse(tmpl.render(RequestContext(request, {
        'mission': mission,
        'game': game,
        'othershoes': othershoes,
        'comment_form': comment_form,
        'player_game': player_game,
    }, [ip])))

@login_required
def comment(request, mission_slug, id, user_id):
    instance = request.user.get_profile().instance
    mission = Mission.objects.get(slug=mission_slug)

    if instance.is_expired() or mission.is_expired():
        return HttpResponseRedirect('/mission/'+ mission_slug +'/game/othershoes/'+ id +'/overview/')

    game = Game.objects.get(id=id)
    othershoes = game.othershoes
    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = othershoes.comments.create(
                message=form.cleaned_data['message'], 
                user=request.user,
                instance=instance,
            )

            if request.POST.has_key('yt-url'):
                if request.POST.get('yt-url'):
                    url = re.search(r"(?<=v=)[a-zA-Z0-9-]+(?=&)|(?<=[0-9]/)[^&\n]+|(?<=v=)[^&\n]+", request.POST.get('yt-url')).group()

                    if len(url) > 1:
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
        else:
            return HttpResponseRedirect('/mission/'+ mission_slug +'/game/othershoes/'+ id +'/'+ user_id +'?error=true')

    return HttpResponseRedirect(reverse('games_othershoes_index', args=[mission_slug, id]))

@login_required
def overview(request, mission_slug, id):
    mission = Mission.objects.get(slug=mission_slug)
    game = get_object_or_404(Game, id=id)
    othershoes = game.othershoes
    first_time = request.session.get('justplayed') or False
    request.session['justplayed'] = False

    if not othershoes.comments.filter(user=request.user).count():
        return HttpResponseRedirect(reverse('games_othershoes_index', args=[mission_slug, id]))

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
    }, [ip])))
