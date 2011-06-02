import web, re 
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext, loader
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from web.missions.models import Mission
from web.games.models import Game, PlayerGame
from web.games.othershoes.models import OtherShoes
from web.responses.comment.models import *
from web.responses.comment.forms import CommentResponseForm
from web.attachments.models import Attachment
from web.comments.models import Comment
from web.comments.forms import CommentForm
from web.reports.actions import PointsAssigner, ActivityLogger
from web.processors import instance_processor as ip

@login_required
def index(request, mission_slug, id):
    instance = request.user.get_profile().instance
    mission = Mission.objects.get(slug=mission_slug)
    game = get_object_or_404(Game, id=id)
    othershoes = game.othershoes

    if instance.is_expired() or mission.is_expired():
        return HttpResponseRedirect('/mission/'+ mission_slug +'/game/othershoes/'+ id +'/overview/')

    player_game = None
 
    # Code to check for games not yet played
    unplayed = []
    _played = []   

    comment_form = CommentResponseForm(instance=othershoes.response)

    if request.method == 'POST':
        comment_form = CommentResponseForm(request.POST, instance=othershoes.response)

        if comment_form.is_valid():
            try:
                player_game = PlayerGame.objects.get(user=request.user, game=game)
                player_game.delete()

                response = CommentResponse(answer=True)
                response.message = comment_form.cleaned_data['message']
                response.save()

                player_game = PlayerGame(visible=True, completed=True, response=response, game=othershoes, user=request.user)
                response = player_game.response.commentresponse
                player_game.save()

                ActivityLogger.log(request.user, request, 'an Other Shoes game', 'updated', '/mission/'+ mission_slug +'/game/othershoes/'+ id +'/'+str(request.user.id), 'othershoes')
            except:
                response = CommentResponse(answer=True)
                response.message = comment_form.cleaned_data['message']
                response.save()
                player_game = PlayerGame(visible=True, completed=True, response=response, game=othershoes, user=request.user)
                player_game.save()
                ActivityLogger.log(request.user, request, 'an Other Shoes game', 'completed', '/mission/'+ mission_slug +'/game/othershoes/'+ id +'/'+str(request.user.id), 'othershoes')
                PointsAssigner.assign(request.user, 'othershoes_completed')

                request.session['justplayed'] = True

            if request.POST.has_key('yt-url'):
                if request.POST.get('yt-url'):
                    url = re.search(r"(?<=v=)[a-zA-Z0-9-]+(?=&)|(?<=[0-9]/)[^&\n]+|(?<=v=)[^&\n]+", request.POST.get('yt-url')).group()

                    if len(url) > 1:
                        response.attachment.create(
                            file=None,
                            url=url,
                            type='video',
                            user=request.user,
                            instance=request.user.get_profile().instance,
                        )

            if request.FILES.has_key('picture'):
                response.attachment.create(
                    file=request.FILES.get('picture'),
                    user=request.user,
                    instance=request.user.get_profile().instance,
                )

            games = mission.games.all()
            pg = PlayerGame.objects.filter(user=request.user, completed=True)
            for p in pg:
                _played.append(p.game)
            for g in games:
                if not g in _played and not g == game:
                    unplayed.append(g)

            return HttpResponseRedirect(request.path +'overview')

    other_responses = PlayerGame.objects.all().filter(game=othershoes, completed=True)

    tmpl = loader.get_template('games/othershoes/index.html')
    return HttpResponse(tmpl.render(RequestContext(request, {
        'unplayed': unplayed,
        'other_responses': other_responses[:5],
        'mission': mission,
        'game': game,
        'othershoes': othershoes,
        'comment_form': comment_form,
        'player_game': player_game,
    }, [ip])))

@login_required
def comment(request, mission_slug, id, user_id):
    a = None
    b = None

    mission = Mission.objects.get(slug=mission_slug)
    game = Game.objects.get(id=id)
    othershoes = game.othershoes
    user = User.objects.get(id=user_id)

    player_game = PlayerGame.objects.filter(user=user, game=game)
    if len(player_game) > 1:
        for pg in player_game[0:len(player_game)-1]:
            pg.delete()

    player_game = player_game[0]

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

            player_game.comments.add(c)
            player_game.save()

            PointsAssigner.assign(request.user, 'comment_created')
            ActivityLogger.log(request.user, request, 'to Other Shoes response', 'added comment', '/mission/'+ mission_slug +'/game/othershoes/'+ id +'/'+ user_id, 'othershoes')
        else:
            return HttpResponseRedirect('/mission/'+ mission_slug +'/game/othershoes/'+ id +'/'+ user_id +'?error=true')

    return HttpResponseRedirect('/mission/'+ mission_slug +'/game/othershoes/'+ id +'/'+ user_id)

@login_required
def overview(request, mission_slug, id):
    mission = Mission.objects.get(slug=mission_slug)
    game = Game.objects.get(id=id)
    othershoes = game.othershoes
    first_time = request.session.has_key('justplayed') and request.session['justplayed'] or False
    request.session['justplayed'] = False

    other_responses = PlayerGame.objects.all().filter(game=othershoes, completed=True)

    responses = []
    for pg in other_responses:
        responses.append(pg)

    unplayed = []
    _played = []
    games = mission.games.all()
    pg = PlayerGame.objects.filter(user=request.user, completed=True)
    for p in pg:
        _played.append(p.game)
    for g in games:
        if not g in _played and not g == game:
            unplayed.append(g)
    
    if len(unplayed):
        unplayed = unplayed[0]

    if othershoes.response and othershoes.response.commentresponse:
        response = othershoes.response.commentresponse
    else:
        response = None
    
    tmpl = loader.get_template('games/othershoes/overview.html')
    return HttpResponse(tmpl.render(RequestContext(request, {
        'other_responses': other_responses[:5],
        'response': response,
        'responses': responses,
        'mission': mission,
        'game': game,
        'othershoes': othershoes,
        'unplayed': unplayed,
        'first_time': first_time,
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
        'response': player_game.response.commentresponse,
        'comment_form': CommentForm(),
    }, [ip])))
