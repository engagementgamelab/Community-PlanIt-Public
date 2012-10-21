from datetime import datetime

from sijax import Sijax
from stream.models import Action

from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

#from django.views.decorators.csrf import ensure_csrf_cookie
#from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
#from django.template import Context, RequestContext, loader
from django.utils.translation import ugettext as _
from django.db.models import Sum
from django.utils.translation import get_language

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from .models import *
from web.core.models import PlayerLeaderboard, AffiliationLeaderboard
from web.accounts.forms import *
from web.accounts.models import *
from web.attachments_v2.models import Attachment
#from web.challenges.models import *
from web.missions.models import *
from web.reports.models import Activity 

import logging
log = logging.getLogger(__name__)


class InstanceDetailView(DetailView):
    model = Instance
    queryset = Instance.objects.exclude(is_disabled=True)

    def get_context_data(self, **kwargs):
        context = super(InstanceDetailView, self).get_context_data(
            **kwargs)
        game = kwargs['object']
        game_profile_exists = False

        log.debug("is auth? %s" % self.request.user.is_authenticated())

        if game.is_future:
            self.template_name = 'instances/instance_future.html'
            #post_reg = bool(self.request.GET.get('post-reg'))

        elif game.is_past:
            self.template_name = 'instances/instance_past.html'
            context['first_mission'] = game.missions[0]

        elif game.is_present:
            self.template_name = 'instances/instance_present.html'

            if self.request.user.is_authenticated():
                # if user is logged in but the active game is not set in the
                # session, log the user out and redirect to the game's log-in page
                active_game = self.request.session.get('my_active_game', None)
                if active_game is None:
                    logout(self.request)
                    return redirect(reverse("instances:login", kwargs={game_slug:game.slug,}))
                context['active_game'] = active_game
                context['active_mission'] = active_game.active_mission

                game_profile_exists = UserProfilePerInstance.objects.filter(
                                            user_profile=self.request.user.get_profile(),
                                            instance=game,
                                        ).exists()


        context['game_profile_exists'] = game_profile_exists
        #context['current_mission'] = game.active_mission
        return context

instance_detail_view = InstanceDetailView.as_view()


class InstanceListView(ListView):
    model = Instance
    template_name = "instances/all.html"

    #def get_context_data(self, **kwargs):
    #    context = super(InstanceListView, self).get_context_data(
    #        **kwargs)
    #    context[''] = ''
    #    return context

instance_list_view = InstanceListView.as_view()


@login_required
def stream(request, template='instances/stream.html'):

    stream_for_game = Action.objects.get_for_target(request.current_game).\
                            filter(verb__in=
                                    [
                                    'activity_completed',
                                    'badge_received',
                                    ]).\
                            order_by('-datetime')
    context = {
        'stream_for_game': stream_for_game[:100],
        'stream_total_count': stream_for_game.count()
    }
    # this line here updates the context with 
    # mission, my_points_for_mission and progress_percentage
    return render(request, template, context)

@login_required
def leaderboard(request, template='instances/leaderboard.html'):
    players_leaderboard = PlayerLeaderboard.objects.for_game(request.current_game)

    try:
        prof_per_instance = UserProfilePerInstance.objects.get(
                    instance=request.current_game, 
                    user_profile=request.user.get_profile()
        )
    except UserProfilePerInstance.DoesNotExist:
        raise Http404("user for this game is not registered")

    try:
        all_names = list(players_leaderboard.values_list('screen_name', flat=True))
        my_name = request.user.get_profile().screen_name 
        my_rank = all_names.index(my_name)+1
        #my_total_points = UserProfilePerInstance.objects.total_points_for_profile(request.current_game, request.user.get_profile())
        my_total_points = prof_per_instance.total_points
    except:
        my_rank = 0
        my_total_points = 0

    affiliations_leaderboard = AffiliationLeaderboard.objects.for_game(request.current_game)

    context = {
        'players_leaderboard': players_leaderboard,
        'affiliations_leaderboard': affiliations_leaderboard,
        'my_rank': my_rank,
        'my_total_points': my_total_points,
    }
    # this line here updates the context with 
    # mission, my_points_for_mission and progress_percentage
    return render(request, template, context)

#@login_required
#def affiliation(request, instance_slug, affiliation_slug, template='affiliations/base.html'):
#    aff = get_object_or_404(Affiliation, slug=affiliation_slug)

#    players = aff.userprofile_set.all()
#    affiliation_points = players.aggregate(Sum('totalPoints'))['totalPoints__sum'] or 0

    #affiliation_leaderboard = []
    #for up in UserProfile.objects.filter(affiliations__contains=aff).order_by("-totalPoints"):
    #    affiliation_leaderboard.append(up.user)
#    affiliation_leaderboard = players.order_by('-totalPoints')

#    context = {
#        'affiliation': aff,
#        'players': players,
#        'affiliation_leaderboard': affiliation_leaderboard,
#        'affiliations_leaderboard': _get_affiliations_leaderboard(),    
#        'affiliation_points': affiliation_points,
#    }
#    return render(request, template, context)


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

#@login_required
#def affiliations_all(request, slug, template='affiliations/all.html'):
#    instance = get_object_or_404(Instance, slug=slug)
    #affiliations = _get_affiliations_leaderboard()
    #affiliations = UserProfile.objects.filter(instance=instance) #.aggregate(Sum('totalPoints'))['totalPoints__sum'] or 0

#    context = {
#            'instance': instance, 
#            'affiliations': instance.affiliations.all().order_by('name')
#    }
#    return render(request, template, context)

#@ensure_csrf_cookie
def ajax_load_games_by_city(request, for_city_id):

    def load_options(obj_response, for_city_id):
        #games_for_city = Instance.objects.filter(for_city__pk=for_city_id).language(get_language())
        games = Instance.objects.exclude(is_disabled=True).filter(for_city__pk=for_city_id).values_list('pk', 'title').distinct().order_by('title')
        out = ""
        for id, title in games:
            out+='<option value="%s">%s</option>' %(id, title)
        obj_response.html('#id_0-instance', out)

    instance = Sijax()
    instance.set_data(request.POST)
    uri = reverse('instances:ajax-load-games-by-city', args=(for_city_id,))
    instance.set_request_uri(uri)
    instance.register_callback('load_games_by_city', load_options)
    if instance.is_sijax_request:
        return HttpResponse(instance.process_request())
    return HttpResponse("")

def ajax_load_languages_by_game(request, instance_id):

    def load_options(obj_response, instance_id):
        game = Instance.objects.get(pk=instance_id)
        langs = game.languages.values_list('pk', 'name').distinct().order_by('code')
        out = ""
        for id, name in langs:
            out+='<option value="%s">%s</option>' %(id, name)
        obj_response.html('#id_0-preferred_language', out)

    instance = Sijax()
    instance.set_data(request.POST)
    uri = reverse('instances:ajax-load-languages-by-game', args=(instance_id,))
    instance.set_request_uri(uri)
    instance.register_callback('load_languages_by_game', load_options)
    if instance.is_sijax_request:
        return HttpResponse(instance.process_request())
    return HttpResponse("")
