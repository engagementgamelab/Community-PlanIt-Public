import datetime
import re

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template import RequestContext, loader
from django.utils import simplejson

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from gmapsfield.fields import GoogleMaps

from web.attachments.models import Attachment
from web.comments.forms import CommentForm
from web.comments.models import Comment
from web.games.mapit.models import Mapit
from web.games.models import Game, PlayerGame
from web.missions.models import Mission
from web.processors import instance_processor as ip
from web.reports.actions import *
from web.responses.map.forms import MapResponseForm
from web.responses.map.models import MapResponse

@login_required
def index(request, mission_slug, id):
    instance = request.user.get_profile().instance
    mission = Mission.objects.get(slug=mission_slug)
    game = get_object_or_404(Game, id=id)
    mapit = game.mapit

    if instance.is_expired() or mission.is_expired():
        return HttpResponseRedirect(reverse('games_mapit_overview', args=[mission_slug, id]))

    unplayed = []
    _played = []

    today = datetime.date.today()
    expired = mission.start_date < today and mission.end_date < today

    player_game = None
    try:
        player_game = PlayerGame.objects.get(user=request.user, game=game)
        map_form = MapResponseForm(instance=mapit.response)
        response = player_game.response.mapresponse
    except:
        map_form = MapResponseForm(instance=mapit.response)
        response = mapit.response

    if request.method == 'POST' and not expired:
        map_form = MapResponseForm(request.POST, instance=mapit.response)

        if map_form.is_valid():

            # delete any existing PlayerGame, adjusting the log message
            # accordingly
            try:
                player_game = PlayerGame.objects.get(user=request.user, game=game)
                player_game.delete()
                log_message = 'updated'
            except PlayerGame.DoesNotExist:
                # this is the first time this player's completed this game
                log_message = 'completed'
                PointsAssigner.assign(request.user, 'mapit_completed')
                request.session['justplayed'] = True

            response = MapResponse(
                answer=True,
                message = map_form.cleaned_data['message'],
                map=map_form.cleaned_data['map']
            )
            response.save()

            player_game = PlayerGame(
                visible=True,
                completed=True,
                response=response,
                game=mapit,
                user=request.user
            )
            player_game.save()

            log_url = reverse('games_mapit_overview', args=[mission_slug, id])
            ActivityLogger.log(request.user, request, 'a MapIT game', log_message, log_url, 'mapit')

            games = mission.games.all()
            pg = PlayerGame.objects.filter(user=request.user, completed=True)
            for p in pg:
                _played.append(p.game)
            for g in games:
                if not g in _played and not g == game:
                    unplayed.append(g)

            return HttpResponseRedirect(reverse('games_mapit_overview', args=[mission_slug, id]))

    other_responses = PlayerGame.objects.all().filter(game=mapit, completed=True)

    tmpl = loader.get_template('games/mapit/index.html')
    return HttpResponse(tmpl.render(RequestContext(request, {
        'unplayed': unplayed,
        'other_responses': other_responses[:5],
        'mission': mission,
        'game': game,
        'mapit': mapit,
        'map_form': map_form,
        'response': response,
        'player_game': player_game,
        'expired': expired,
    }, [ip])))

@login_required
def overview(request, mission_slug, id):
    mission = Mission.objects.get(slug=mission_slug)
    game = get_object_or_404(Game, id=id)
    mapit = game.mapit
    first_time = request.session.has_key('justplayed') and request.session['justplayed'] or False
    request.session['justplayed'] = False
    
    other_responses = PlayerGame.objects.all().filter(game=mapit, completed=True)
    
    if not mapit.playergame_set.filter(user=request.user).count():
        messages.success(request, "You'll have to complete this activity to join its discussion.", extra_tags='sticky')
        return HttpResponseRedirect(reverse('games_mapit_index', args=[mission_slug, id]))

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = mapit.comments.create(
                message=comment_form.cleaned_data['message'], 
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
            log_url = reverse('games_mapit_overview', args=[mission_slug, id]) + '#comment-' + str(comment.pk)
            ActivityLogger.log(request.user, request, 'to MapIT response', 'added comment', log_url, 'mapit')

            return HttpResponseRedirect(reverse('games_mapit_overview', args=[mission_slug, id]))
    else:
        comment_form = CommentForm()

    respondents = []
    for pg in other_responses:
        respondents.append({
            'player': pg.user.get_profile()
        })
    
    markers = []
    for pg in other_responses:
        _markers = pg.response.mapresponse.map.markers

        if _markers:
            for marker in _markers:
                try: 
                    marker['message'] = pg.response.mapresponse.message
                    marker['player'] = pg.user.get_profile().screen_name()
                except: pass
            markers.append(_markers)

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
    
    
    tmpl = loader.get_template('games/mapit/overview.html')
    return HttpResponse(tmpl.render(RequestContext(request, {
        'other_responses': other_responses[:5],
        'response': mapit.response.mapresponse,
        'markers': simplejson.dumps(markers),
        'mission': mission,
        'game': game,
        'mapit': mapit,
        'respondents': respondents,
        'unplayed': unplayed,
        'first_time': first_time,
    },[ip])))


@login_required
def response(request, mission_slug, id, user_id):
    mission = Mission.objects.get(slug=mission_slug)
    game = Game.objects.get(id=id)
    mapit = game.mapit
    user = User.objects.get(id=user_id)

    player_game = PlayerGame.objects.get(user=user, game=game)

    other_responses = PlayerGame.objects.all().filter(game=mapit, completed=True)

    tmpl = loader.get_template('games/mapit/response.html')
    return HttpResponse(tmpl.render(RequestContext(request, {
        'other_responses': other_responses[:5],
        'mission': mission,
        'game': game,
        'mapit': mapit,
        'user': user,
        'player_game': player_game,
        'comments': player_game,
        'response': player_game.response.mapresponse,
        'comment_form': CommentForm(),
    }, [ip])))

