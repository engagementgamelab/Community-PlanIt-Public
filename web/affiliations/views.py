import datetime
from django.core.mail import send_mail

from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, RequestContext, loader
from django.shortcuts import render, get_object_or_404
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from web.core.models import AffiliationLeaderboard
from web.instances.models import Affiliation
from web.accounts.forms import UserProfileVariantsForInstance

from web.core.utils import missions_bar_context

@login_required
def all(request, template="affiliations/all.html"):

    if not hasattr(request, 'current_game'):
        raise Http404("could not locate a valid game")

    #def _get_affiliations_leaderboard():
    #    affiliations = []  
    #    for user in UserProfile.objects.all().order_by("-totalPoints"):        
    #        if user.affiliations is not None:
    #            user_affiliations = user.affiliations.split(', ')
    #            for affiliation in user_affiliations:
    #                if affiliation != u'':
    #                    if not affiliation.strip() == '' and not affiliation in affiliations:
    #                        affiliations.append(affiliation)    
    #    return affiliations

    variants_for_game = UserProfileVariantsForInstance.objects.get(instance=request.current_game)
    affiliations =  variants_for_game.affiliation_variants.all()
    context = {
        'affiliations': affiliations,
    }
    context.update(missions_bar_context(request))
    return render(request, template, context)

@login_required
def affiliation(request, slug, template='affiliations/affiliation.html'):

    if not hasattr(request, 'current_game'):
        raise Http404("could not locate a valid game")

    affiliation = get_object_or_404(Affiliation, slug=slug)
    leaderboard_entry = AffiliationLeaderboard.objects.get(instance=request.current_game, affiliation=affiliation)
    #players = UserProfilePerInstance.objects.all_by_affiliation(request.current_game, slug)
    players = affiliation.user_profiles_per_instance.filter(instance=request.current_game).order_by('user_profile__user__first_name')
    #total_points = 0
    #for player in players:
    #    total_points+=UserProfilePerInstance.objects.total_points_for_profile(request.current_game, player)
    #total_points = UserProfilePerInstance.objects.total_points_by_affiliation(request.current_game, slug)

    context = {
        'affiliation': affiliation,
        'players': players,
        'total_points': leaderboard_entry.points,
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


