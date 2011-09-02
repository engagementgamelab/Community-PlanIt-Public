from nani.utils import get_translation

from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

from instances.models import Instance
from missions.models import Mission

from admin.views import verify
from admin.forms import MissionForm

import logging
log = logging.getLogger(__name__)

@login_required
def manage(request, instance_id, template="admin/manage_missions.html"):
    ok = verify(request)
    if ok != None:
        return ok
    #TODO: Make the instances only be drawn from instances that the user supervises

    try:
        instance = Instance.objects.untranslated().get(pk=int(instance_id))
    except Instance.DoesNotExist:
        raise Http404 ("Instance with id %s does not exist" % instance_id)

    data = {}
    for mission in Mission.objects.untranslated().filter(instance=instance):
        data[mission] = {
                'mission_translations': mission.translations.all(),
        }
    context = {
        'data' : data,
        'instance' : instance,
    }
    return render_to_response(template, RequestContext(request, context))


@login_required
def mission(request, instance_id, mission_id=None, template="admin/trans_mission_edit_new.html"):
    is_new = False
    ok = verify(request)
    if ok != None:
        return ok

    try:
        instance = Instance.objects.untranslated().get(pk=int(instance_id))
    except Instance.DoesNotExist:
        raise Http404 ("Instance with id %s does not exist" % instance_id)

    if (request.POST.has_key("submit_btn") and request.POST["submit_btn"] == "Cancel"):
        return HttpResponseRedirect(reverse("admin:manage-missions", args=[instance_id]))

    if mission_id is not None and mission_id != 'None':
        try:
            mission = Mission.objects.untranslated().get(pk=int(mission_id))
        except Mission.DoesNotExist:
            raise Http404 ("Mission with id %s does not exist" % mission_id)
    else:
        mission = None
        is_new = True

    errors = {}
    form = MissionForm(mission_instance=instance, instance=mission, data=request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            try:
                mission = form.save(commit=False)
            except Exception, err:
                #transaction.rollback()
                print "error while saving mission: %s" % str(err)
                log.error("error while saving mission: %s" % str(err))
                errors.update({"Updating mission": "Server error took place. Please contact the admin."})
            else:
                #transaction.commit()
                return HttpResponseRedirect(reverse("admin:manage-missions", args=[instance_id]))
        else:
            for f in form.inner_trans_forms:
                if f.errors:
                    errors.update(f.errors)
            if form.errors:
                errors.update(form.errors)

    context = {
            'mission': mission,
            'instance': instance,
            'mission_form': form,
            'new': is_new,
            'errors': errors,
    }

    return render_to_response(template, RequestContext(request, context))


@login_required
def new(request, instance_id):
    return mission(request, instance_id)

@login_required
def delete(request, mission_id):
    pass



