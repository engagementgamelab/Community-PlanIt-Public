from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import Context, RequestContext, loader

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from accounts.models import UserProfile
from instances.models import Instance
from values.models import *

@login_required
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
    }, #[ip]
    )))

@login_required
def instance(request, slug):
    instance = Instance.objects.get(slug=slug)
    players = UserProfile.objects.filter(user__is_active=True, instance=instance)

    return display_list(request, players, instance.title +' Community')
