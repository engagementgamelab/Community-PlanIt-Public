import datetime
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, RequestContext, loader
from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from instances.models import *
from accounts.models import *
from missions.models import *
from challenges.models import *
from accounts.forms import *

from web.core.utils import missions_bar_context

@login_required
def all(request, template="affiliations/all.html"):
    context = {
        'affiliations': Affiliation.objects.all()
    }
    
    context.update(missions_bar_context(request))
    return render(request, template, context)

    # tmpl = loader.get_template('affiliations/all.html')
    # affiliations = _get_affiliations_leaderboard()               
    # return HttpResponse(tmpl.render(RequestContext(request, { 'affiliations': affiliations},))
    # )

@login_required
def affiliation(request, slug, template='affiliations/affiliation.html'):
    try: 
        affiliation = Affiliation.objects.get(slug=slug)
    except:
        affiliation = None
    
    context = {
        'affiliation': affiliation,
    }
    
    context.update(missions_bar_context(request))
    return render(request, template, context)
    # aff = request.GET.get('aff', '')
    # if not aff:
    #     return Http404("affiliation could not be located")
    # 
    # players = UserProfile.objects.select_related('user').filter(affiliations__contains=aff)
    # 
    # affiliation_points = players.aggregate(Sum('totalPoints'))['totalPoints__sum'] or 0
    # 
    # 
    # #affiliation_leaderboard = []
    # #for up in UserProfile.objects.filter(affiliations__contains=aff).order_by("-totalPoints"):
    # #    affiliation_leaderboard.append(up.user)
    # affiliation_leaderboard = players.order_by('-totalPoints')
    # 
    # 
    # tmpl = loader.get_template('affiliations/base.html')
    # return HttpResponse(tmpl.render(RequestContext(request, {
    #     'affiliation': aff,
    #     'players': players,
    #     'affiliation_leaderboard': affiliation_leaderboard,
    #     'affiliations_leaderboard': _get_affiliations_leaderboard(),    
    #     'affiliation_points': affiliation_points,
    # }, 
    # #[ip]
    # )))

def _get_affiliations_leaderboard():
    affiliations = []  
    for user in UserProfile.objects.all().order_by("-totalPoints"):        
        if user.affiliations is not None:
            user_affiliations = user.affiliations.split(', ')
            for affiliation in user_affiliations:
                if affiliation != u'':
                    if not affiliation.strip() == '' and not affiliation in affiliations:
                        affiliations.append(affiliation)    
    return affiliations


