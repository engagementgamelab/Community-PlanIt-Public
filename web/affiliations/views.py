from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from web.core.models import AffiliationLeaderboard
from web.instances.models import Affiliation
from web.accounts.forms import UserProfileVariantsForInstance

@login_required
def all(request, template="affiliations/all.html"):

    if not hasattr(request, 'current_game'):
        raise Http404("could not locate a valid game")

    variants_for_game = UserProfileVariantsForInstance.objects.get(instance=request.current_game)
    affiliations =  variants_for_game.affiliation_variants.all()
    context = {
        'affiliations': affiliations,
    }
    return render(request, template, context)

@login_required
def affiliation(request, slug, template='affiliations/affiliation.html'):

    if not hasattr(request, 'current_game'):
        raise Http404("could not locate a valid game")

    #affiliation = get_object_or_404(Affiliation, slug=slug)

    qs = Affiliation.objects.filter(slug=slug)
    if qs.count() > 0:
        affiliation = qs[0]
    else:
        raise Http404("Affiliation could not be found.")

    leaderboard_entry = AffiliationLeaderboard.objects.get(instance=request.current_game, affiliation=affiliation)
    players = affiliation.user_profiles_per_instance.filter(instance=request.current_game).order_by('user_profile__user__first_name')

    context = {
        'affiliation': affiliation,
        'players': players,
        'total_points': leaderboard_entry.points,
    }

    return render(request, template, context)



