import datetime

from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, RequestContext, loader
from django.contrib import auth

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from web.instances.models import *
from web.attachments.models import Attachment
from web.accounts.models import *
from web.missions.models import *
from web.challenges.models import *
from web.accounts.forms import *
from web.reports.models import Activity 
from web.reports.actions import ActivityLogger
from web.processors import instance_processor as ip

def region(request, slug):
    instance = Instance.objects.get(slug=slug)

    users = User.objects.filter(userprofile__instance=instance)
    leaderboard = users.order_by('-userprofile__points')
    log = Activity.objects.filter(instance=instance).order_by('-date')[:100]
    attachments = Attachment.objects.filter(instance=instance).exclude(file='')

    tmpl = loader.get_template('instances/base.html')
    return HttpResponse(tmpl.render(RequestContext(request, {
        'current_instance': instance,
        'users': users,
        'leaderboard': leaderboard,
        'log': log,
        'attachments': attachments,
    }, [ip])))

def all(request):
    instances = Instance.objects.all()
    today = datetime.date.today()
    
    # Get number of players in instance
    for instance in instances:
        instance.player_count = 0
        instance_users = User.objects.filter(userprofile__instance=instance)
        for user in instance_users:
            instance.player_count += 1

    tmpl = loader.get_template('instances/all.html')
    return HttpResponse(tmpl.render(RequestContext(request, {
        'instances': instances,
        'today': today,
    }, [ip])))
