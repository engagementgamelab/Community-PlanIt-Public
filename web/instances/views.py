import datetime

from sijax import Sijax

from django.contrib import auth
from django.views.decorators.csrf import ensure_csrf_cookie
#from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
#from django.template import Context, RequestContext, loader
from django.utils.translation import ugettext as _
from django.db.models import Sum
from django.utils.translation import get_language

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from accounts.forms import *
from accounts.models import *
from attachments.models import Attachment
from challenges.models import *
from instances.forms import NotificationRequestForm
from instances.models import *
from missions.models import *
from reports.models import Activity 
from core.utils import get_translation_with_fallback

#TODO: this does not fail nicely, it should 
def region(request, slug):
    community = get_object_or_404(Instance, slug=slug)

    if request.method == 'POST':
        notification_form = NotificationRequestForm(community, request.POST)
        if notification_form.is_valid():
            notification_request = notification_form.save(commit=False)
            try:
                # if we have one, we can still give them the success message
                existing_request = NotificationRequest.objects.get(instance=community, email=notification_request.email)
            except NotificationRequest.DoesNotExist:
                # good
                notification_request.instance = community
                notification_request.save()
            messages.success(request, _("We'll let you know when {0} is active. Thanks for your interest!").format(community))
            return redirect(reverse('instances'))
    else:
        notification_form = NotificationRequestForm(community)

    #userProfiles = UserProfile.objects.filter(instance=community)
    #users = []
    #for userProfile in userProfiles:
    #    users.append(userProfile.user)
    #leaderboard = []
    #for userProfile in userProfiles.order_by("-totalPoints"):
    #    leaderboard.append(userProfile.user)
    #log = Activity.objects.filter(instance=community).order_by('-date')[:100]
    attachments = Attachment.objects.filter(instance=community).exclude(file='')

    data = {
        'notification_form': notification_form,
        'community': community,
        #'users': users,
        #'leaderboard': leaderboard,
        #'log': log,
        'attachments': attachments,
    }
    return render(request, 'instances/base.html', data)

def all(request):
    kwargs=dict(
            for_city__domain=request.current_site.domain,
    )
    active = Instance.objects.active().filter(**kwargs)
    future = Instance.objects.future().filter(**kwargs)
    past = Instance.objects.past().filter(**kwargs)

    context = {
        'active': active,
        'future': future,
        'past': past,
    }
    return render(request, 'instances/all.html', context)

@login_required
def stream(request, template='instances/stream.html'):

    response = {}

    return render(request, template, response)

@login_required
def leaderboard(request, template='instances/leaderboard.html'):

    response = {}
        # 'affiliations_leaderboard': _get_affiliations_leaderboard(), 

    return render(request, template, response)

@login_required
def affiliation(request, instance_slug, affiliation_slug, template='affiliations/base.html'):
    aff = get_object_or_404(Affiliation, slug=affiliation_slug)

    players = aff.userprofile_set.all()
    affiliation_points = players.aggregate(Sum('totalPoints'))['totalPoints__sum'] or 0

    #affiliation_leaderboard = []
    #for up in UserProfile.objects.filter(affiliations__contains=aff).order_by("-totalPoints"):
    #    affiliation_leaderboard.append(up.user)
    affiliation_leaderboard = players.order_by('-totalPoints')

    context = {
        'affiliation': aff,
        'players': players,
        'affiliation_leaderboard': affiliation_leaderboard,
        'affiliations_leaderboard': _get_affiliations_leaderboard(),    
        'affiliation_points': affiliation_points,
    }
    return render(request, template, context)


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

@login_required
def affiliations_all(request, slug, template='affiliations/all.html'):
    instance = get_object_or_404(Instance, slug=slug)
    #affiliations = _get_affiliations_leaderboard()
    #affiliations = UserProfile.objects.filter(instance=instance) #.aggregate(Sum('totalPoints'))['totalPoints__sum'] or 0

    context = {
            'instance': instance, 
            'affiliations': instance.affiliations.all().order_by('name')
    }
    return render(request, template, context)

#@ensure_csrf_cookie
def ajax_load_games_by_city(request, for_city_id):

    def load_options(obj_response, for_city_id):
        games_for_city = Instance.objects.filter(for_city__pk=for_city_id).language(get_language())
        games = [(x.pk, get_translation_with_fallback(x, 'title')) for x in games_for_city]
        out = ""
        for id, title in games:
            out+='<option value="%s">%s</option>' %(id, title)
        obj_response.html('#id_0-instance', out)

    instance = Sijax()
    instance.set_data(request.POST)
    load_games_uri = reverse('instances:ajax-load-games-by-city', args=(for_city_id,))
    instance.set_request_uri(load_games_uri)
    instance.register_callback('load_games_by_city', load_options)
    if instance.is_sijax_request:
        return HttpResponse(instance.process_request())
    return HttpResponse("")
