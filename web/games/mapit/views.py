import re, web, datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import simplejson
from django.shortcuts import get_object_or_404
from web.attachments.models import Attachment
from web.missions.models import Mission
from web.games.models import Game, PlayerGame
from web.games.mapit.models import Mapit
from web.responses.map.models import MapResponse
from web.responses.map.forms import MapResponseForm
from web.comments.models import Comment
from web.comments.forms import CommentForm
from web.reports.actions import *
from gmapsfield.fields import GoogleMaps
from web.processors import instance_processor as ip

@login_required
def index(request, mission_slug, id):
    instance = request.user.get_profile().instance
    mission = Mission.objects.get(slug=mission_slug)
    game = get_object_or_404(Game, id=id)
    mapit = game.mapit

    if instance.is_expired() or mission.is_expired():
        return HttpResponseRedirect('/mission/'+ mission_slug +'/game/othershoes/'+ id +'/overview/')

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

            # Replay
            try:
                player_game = PlayerGame.objects.get(user=request.user, game=game)
                player_game.delete()

                c = Comment(
                    message=map_form.cleaned_data['message'], 
                    user=request.user,
                    instance=request.user.get_profile().instance,
                )
                c.save()
                response = MapResponse(answer=True, map=map_form.cleaned_data['map'])
                response.save()
                response.comments.add(c)
                response.save()

                player_game = PlayerGame(visible=True, completed=True, response=response, game=mapit, user=request.user)
                response = player_game.response.mapresponse
                player_game.save()

                ActivityLogger.log(request.user, request, 'a MapIT game', 'updated', '/mission/'+ mission_slug +'/game/mapit/'+ id +'/'+str(request.user.id), 'mapit')
                
            # Play for the first time
            except:
                response = MapResponse(answer=True, map=map_form.cleaned_data['map'])
                response.save()

                c = Comment(
                    message=map_form.cleaned_data['message'], 
                    user=request.user,
                    instance=request.user.get_profile().instance,
                )
                c.save()
                response.comments.add(c)
                response.save()

                player_game = PlayerGame(visible=True, completed=True, response=response, game=mapit, user=request.user)
                response = player_game.response.mapresponse
                player_game.save()

                ActivityLogger.log(request.user, request, 'a MapIT game', 'completed', '/mission/'+ mission_slug +'/game/mapit/'+ id +'/'+str(request.user.id), 'mapit')
                PointsAssigner.assign(request.user, 'mapit_completed')

                request.session['justplayed'] = True


            games = mission.games.all()
            pg = PlayerGame.objects.filter(user=request.user, completed=True)
            for p in pg:
                _played.append(p.game)
            for g in games:
                if not g in _played and not g == game:
                    unplayed.append(g)

            return HttpResponseRedirect(request.path +'overview')
                

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
def comment(request, mission_slug, id, user_id):
    a = None
    b = None

    mission = Mission.objects.get(slug=mission_slug)
    game = Game.objects.get(id=id)
    mapit = game.mapit
    user = User.objects.get(id=user_id)
    instance = request.user.get_profile().instance

    player_game = PlayerGame.objects.filter(user=user, game=game)
    if len(player_game) > 1:
        for pg in player_game[0:len(player_game)-1]:
            pg.delete()

    player_game = player_game[0]

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            c = Comment(
                message=form.cleaned_data['message'], 
                user=request.user,
                instance=instance,
            )
            c.save()
            player_game.comments.add(c)
            player_game.save()

            PointsAssigner.assign(request.user, 'comment_created')
            ActivityLogger.log(request.user, request, 'to MapIT response', 'added comment', '/mission/'+ mission_slug +'/game/mapit/'+ id +'/'+ user_id, 'mapit')

            if request.POST.has_key('yt-url'):
                if request.POST.get('yt-url'):
                    url = re.search(r"(?<=v=)[a-zA-Z0-9-]+(?=&)|(?<=[0-9]/)[^&\n]+|(?<=v=)[^&\n]+", request.POST.get('yt-url')).group()

                    if len(url) > 1:
                        c.attachment.create(
                            file=None,
                            url=url,
                            type='video',
                            user=request.user,
                            instance=request.user.get_profile().instance,
                        )

            if request.FILES.has_key('picture'):
                c.attachment.create(
                    file=request.FILES.get('picture'),
                    user=request.user,
                    instance=request.user.get_profile().instance,
                )

    return HttpResponseRedirect('/mission/'+ mission_slug +'/game/mapit/'+ id +'/'+ user_id)

@login_required
def overview(request, mission_slug, id):
    mission = Mission.objects.get(slug=mission_slug)
    game = get_object_or_404(Game, id=id)
    mapit = game.mapit
    first_time = request.session.has_key('justplayed') and request.session['justplayed'] or False
    request.session['justplayed'] = False
    
    other_responses = PlayerGame.objects.all().filter(game=mapit, completed=True)
    
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
                    marker['message'] = pg.response.mapresponse.comments.all()[0].message
                    marker['player'] = pg.user.get_profile().first_name + " " + pg.user.get_profile().last_name[:1]
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
    game = get_object_or_404(Game, id=id)
    mapit = game.mapit
    user = User.objects.get(id=user_id)

    player_game = PlayerGame.objects.filter(user=user, game=game)
    if len(player_game) > 1:
        for pg in player_game[0:len(player_game)-1]:
            pg.delete()

    player_game = player_game[0]

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
    },[ip])))
