import datetime
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, RequestContext, loader
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from web.instances.models import *
from web.accounts.models import *
from web.missions.models import *
from web.challenges.models import *
from web.accounts.forms import *
from web.reports.actions import ActivityLogger
#from web.processors import instance_processor as ip

@login_required
def affiliation(request, affiliation):
    instance = request.user.get_profile().instance
    users = []
    for up in UserProfile.objects.filter(instance=instance):
        users.append(up.user)

    players = []
    for up in UserProfile.objects.filter(affiliations__contains=affiliation):
        players.append(up.user)
    
    affiliation_leaderboard = []
    for up in UserProfile.objects.filter(affiliations__contains=affiliation).order_by("-totalPoints"):
        affiliation_leaderboard.append(up.user)
    
    affiliation_points = 0
    
    for player in players:
        affiliation_points += player.get_profile().totalPoints    
    
    tmpl = loader.get_template('affiliations/base.html')
    return HttpResponse(tmpl.render(RequestContext(request, {
        'affiliation': affiliation,
        'players': players,
        'affiliation_leaderboard': affiliation_leaderboard,
        'affiliations_leaderboard': _get_affiliations_leaderboard(),    
        'affiliation_points': affiliation_points,
    }, 
    #[ip]
    )))
    
    
def _get_affiliations_leaderboard():
    affiliations = []  
    for user in UserProfile.objects.all().order_by("-totalPoints"):        
        user_affiliations = user.affiliations.split(', ')
        for affiliation in user_affiliations:            
            if not affiliation.strip() == '' and not affiliation in affiliations:
                affiliations.append(affiliation)    
    return affiliations                    


@login_required
def all(request):
    tmpl = loader.get_template('affiliations/all.html')
    affiliations = _get_affiliations_leaderboard()               
    return HttpResponse(tmpl.render(RequestContext(request, {
                            'affiliations': affiliations
                        }, 
                            #[ip]
                    )))
