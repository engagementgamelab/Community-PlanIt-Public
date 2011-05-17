import datetime
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import Context, RequestContext, loader
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from web.missions.models import *
from web.instances.models import Instance
from web.comments.models import Comment
from web.comments.forms import CommentForm
from web.games.models import PlayerGame
from web.processors import instance_processor as ip

@login_required
def fetch(request, slug):
    # Mission detail
    try:
        mission = Mission.objects.get(slug=slug)
    except:
        raise Http404

    player_games = PlayerGame.objects.filter(visible=True, completed=True, user=request.user)

    if mission.end_date < datetime.date.today():
        active = False
    else:
        active = True

    games = []
    
    for pg in player_games:
        games.append(pg.game)
    
    tmpl = loader.get_template('missions/base.html')
    return HttpResponse(tmpl.render(RequestContext(request, {
        'mission': mission,
        'games': games,
        'comment_form': CommentForm(),
        'active': active,
    }, [ip])))

@login_required
def all(request):
    player_games = PlayerGame.objects.filter(visible=True, completed=True, user=request.user)
    played = []

    for pg in player_games:
        played.append(pg.game)

    tmpl = loader.get_template('missions/all.html')
    return HttpResponse(tmpl.render(RequestContext(request, {
        'played': played,
    }, [ip])))
