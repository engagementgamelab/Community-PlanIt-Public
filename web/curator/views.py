import csv
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils import simplejson
from django.core import serializers
from web.issues.models import *
from web.instances.models import *
from web.accounts.models import *
from web.missions.models import *
from web.games.models import *
from web.issues.models import *
from web.challenges.models import *
from web.comments.models import *
from web.reports.models import *
from django.contrib.auth.decorators import login_required

@login_required
def admin(request, id):
    try:
        instance = Instance.objects.get(id=id)

        if request.user == instance.curator:
            request.session['admin_instance'] = instance

        return HttpResponseRedirect('/admin')
    except:
        return Http404

@login_required
def instance(request, id):
    try:
        instance = Instance.objects.get(id=id)
        request.session['admin_instance'] = instance

        return HttpResponse('success')
    except:
        return HttpResponse('failure')

@login_required
def all_instances(request):
    instances = []
    i = Instance.objects.all()

    if request.user.is_superuser:
        for instance in i:
            if request.session.has_key('admin_instance') and instance == request.session['admin_instance']:
                instances.append({ 'id': instance.id, 'region': instance.region, 'selected': True })
            else:
                instances.append({ 'id': instance.id, 'region': instance.region, 'selected': False })

        if not request.session.has_key('admin_instance'):
            request.session['admin_instance'] = i[0]
    else:
        for instance in i:
            if request.user.get_profile().instance == instance:
                instances.append({ 'id': instance.id, 'region': instance.region, 'selected': True })

    return HttpResponse(simplejson.dumps(instances))

@login_required
def all_flagged(request):
    flagged = []

    def add_flagged(label, count, url):
        flagged.append({ 'label': label, 'count': count, 'url': url })

    u = User.objects.filter(userprofile__flagged__gt=0, instance=request.session['admin_instance']).order_by("-userprofile__flagged")

    for user in u:
        add_flagged(user.get_profile().first_name + " " + user.get_profile().last_name, user.get_profile().flagged, '/admin/auth/user/'+ str(user.id))

    c = Comment.objects.filter(flagged__gt=0, instance=request.session['admin_instance']).order_by("-flagged")

    for comment in c:
        add_flagged(comment.message, comment.flagged, '/admin/comments/comment/'+ str(comment.id))

    ch = Challenge.objects.filter(flagged__gt=0, instance=request.session['admin_instance']).order_by("-flagged")
    
    for challenge in ch:
        add_flagged(challenge.name, challenge.flagged, '/admin/challenges/challenge/'+ str(challenge.id))

    return HttpResponse(simplejson.dumps(flagged))

@login_required
def set_pk(request, id):
    request.session['admin_pk'] = id

@login_required
def all_attachments(request):
    a = Attachment.objects.all()

    return HttpResponse(serializers.serialize('json', a))

@login_required
def generate_csv(request, model):
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment;filename="'+ model +'.csv"'

    writer = csv.writer(response)
    instance = request.session['admin_instance']

    if model == 'userprofile':
        objects = UserProfile.objects.filter(instance=instance)
    elif model == 'activity':
        objects = Activity.objects.filter(instance=instance)

    i = 0
    for obj in objects:
        if i == 0: writer.writerow(obj.__dict__.keys())
        i = i+1

        writer.writerow(obj.__dict__.values())

    return response
