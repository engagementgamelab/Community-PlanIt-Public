import datetime

from django.contrib import auth
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import Context, RequestContext, loader
from django.utils.translation import ugettext as _

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from web.accounts.forms import *
from web.accounts.models import *
from web.attachments.models import Attachment
from web.challenges.models import *
from web.instances.forms import NotificationRequestForm
from web.instances.models import *
from web.missions.models import *
#from web.processors import instance_processor as ip
from web.reports.actions import ActivityLogger
from web.reports.models import Activity 

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
            return HttpResponseRedirect(reverse('instances'))
    else:
        notification_form = NotificationRequestForm(community)

    userProfiles = UserProfile.objects.filter(instance=community)
    users = []
    for userProfile in userProfiles:
        users.append(userProfile.user)
    leaderboard = []
    for userProfile in userProfiles.order_by("-totalPoints"):
        leaderboard.append(userProfile.user)
    log = Activity.objects.filter(instance=community).order_by('-date')[:100]
    attachments = Attachment.objects.filter(instance=community).exclude(file='')

    data = {
        'notification_form': notification_form,
        'community': community,
        'users': users,
        'leaderboard': leaderboard,
        'log': log,
        'attachments': attachments,
    }
    return render_to_response('instances/base.html', data, context_instance=RequestContext(request))

def all(request):
    mgr = Instance.objects
    now = datetime.datetime.now()

    # Get number of players in instance
    #for instance in instances:
    #    instance.player_count = UserProfile.objects.filter(instance=instance).count()
    #    print instance.player_count

    #tmpl = loader.get_template('instances/all.html')

    data = {
        'mgr': mgr,
        'now': now,
    }
    return render_to_response('instances/all.html', data, context_instance=RequestContext(request))
