import datetime
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import Context, RequestContext, loader
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from web.instances.models import Instance
from web.accounts.models import UserProfile
from web.issues.models import *
from web.reports.actions import ActivityLogger, PointsAssigner
from web.processors import instance_processor as ip

def display_list(request, players, title):
    p = Paginator(players, 10)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        players = p.page(page)
    except:
        players = p.page(p.num_pages)
    
    tmpl = loader.get_template('lists/list.html')
    return HttpResponse(tmpl.render(RequestContext(request, {
        'page': title,
        'players': players,
    }, [ip])))

@login_required
def instance(request, slug):
    instance = Instance.objects.get(slug=slug)
    players = User.objects.filter(is_active=True)

    return display_list(request, players, instance.name +' Neighborhood')

@login_required
def following(request, id):
    player = User.objects.get(id=id)
    players = player.get_profile().following.all()

    return display_list(request, players, player.first_name +' is following')

def followers(request, id):

    player = User.objects.get(id=id)
    players = []

    for p in User.objects.select_related():
        try:
            if player and player.get_profile() and player in p.get_profile().following.all():
                players.append(p)
        except:
            pass

    return display_list(request, players, player.first_name +' followers')
