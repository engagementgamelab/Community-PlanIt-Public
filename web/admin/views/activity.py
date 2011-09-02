from nani.utils import get_translation

from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

from instances.models import Instance
from player_activities.models import PlayerActivity

from admin.views import verify
from admin.forms import ActivityForm

import logging
log = logging.getLogger(__name__)

@login_required
def manage(request, instance_id, template="admin/manage_activities.html"):
    ok = verify(request)
    if ok != None:
        return ok
    #TODO: Make the instances only be drawn from instances that the user supervises

    try:
        instance = Instance.objects.untranslated().get(pk=int(instance_id))
    except Instance.DoesNotExist:
        raise Http404 ("Instance with id %s does not exist" % instance_id)

    data = {}
    for activity in PlayerActivity.objects.untranslated().filter(instance=instance):
        data[activity] = {
                'activity_translations': activity.translations.all(),
        }
    context = {
        'data' : data,
        'instance' : instance,
    }
    return render_to_response(template, RequestContext(request, context))


@login_required
def activity(request, instance_id, activity_id=None, template="admin/trans_activity_edit_new.html"):
    is_new = False
    ok = verify(request)
    if ok != None:
        return ok

    try:
        instance = Instance.objects.untranslated().get(pk=int(instance_id))
    except Instance.DoesNotExist:
        raise Http404 ("Instance with id %s does not exist" % instance_id)

    if (request.POST.has_key("submit_btn") and request.POST["submit_btn"] == "Cancel"):
        return HttpResponseRedirect(reverse("admin:manage-activities", args=[instance_id]))

    if activity_id is not None and activity_id != 'None':
        try:
            activity = PlayerActivity.objects.untranslated().get(pk=int(activity_id))
        except Activity.DoesNotExist:
            raise Http404 ("Player Activity with id %s does not exist" % activity_id)
    else:
        activity = None
        is_new = True

    errors = {}
    form = ActivityForm(activity_instance=instance, instance=activity, data=request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            try:
                activity = form.save(commit=False)
            except Exception, err:
                #transaction.rollback()
                print "error while saving activity: %s" % str(err)
                log.error("error while saving activity: %s" % str(err))
                errors.update({"Updating activity": "Server error took place. Please contact the admin."})
            else:
                #transaction.commit()
                return HttpResponseRedirect(reverse("admin:manage-activities", args=[instance_id]))
        else:
            for f in form.inner_trans_forms:
                if f.errors:
                    errors.update(f.errors)
            if form.errors:
                errors.update(form.errors)

    context = {
            'activity': activity,
            'instance': instance,
            'activity_form': form,
            'new': is_new,
            'errors': errors,
    }

    return render_to_response(template, RequestContext(request, context))


@login_required
def new(request, instance_id):
    return activity(request, instance_id)

@login_required
def delete(request, activity_id):
    pass



