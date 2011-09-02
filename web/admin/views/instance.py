from nani.utils import get_translation

import datetime

from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseServerError
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.utils import simplejson

from instances.models import Instance
from admin.views import verify
from admin.forms import InstanceForm

import logging
log = logging.getLogger(__name__)

def trans_for_instance(instance):
    return [get_translation(instance, lang) for lang in instance.get_available_languages()]

#*************************
# INSTANCE RELATED VIEWS
@login_required
def manage(request, template="admin/manage_game.html"):
    ok = verify(request)
    if ok != None:
        return ok
    #TODO: Make the instances only be drawn from instances that the user supervises

    if request.user.is_superuser:
        instances_all = Instance.objects.untranslated().all().order_by("start_date")
    else:
        instances_all = Instance.objects.untranslated().filter(curators=request.user).order_by("start_date")

    instances_data = {}
    for instance in instances_all:
        #Value.objects.untranslated().filter(instance=instance)
        instances_data[instance] = {
                'instance_translations': instance.translations.all(),
                #'instance_translations': trans_for_instance(instance),
        }
    context = {
        'instances_data' : instances_data,
    }
    return render_to_response(template, RequestContext(request, context))

@login_required
#@transaction.commit_manually
def instance(request, instance_id=None, template="admin/trans_instance_edit.html"):
    is_new = False
    ok = verify(request)
    if ok != None:
        return ok

    if (request.POST.has_key("submit_btn") and request.POST["submit_btn"] == "Cancel"):
        return HttpResponseRedirect(reverse("admin-base"))

    #FIXME
    # what is with this instance_id? 
    # why is it 'None' coming from  `new instance` form?
    if instance_id is not None and instance_id != 'None':
        try:
            inst = Instance.objects.untranslated().get(pk=instance_id)
        except Instance.DoesNotExist:
            raise Http404 ("instance with id %s does not exist" % instance_id)
    else:
    	inst = Instance(start_date=datetime.datetime.now())
    	is_new = True

    init_coords = []
    if inst.location:
        markers = simplejson.loads("%s" % inst.location)["markers"]
        x = 0
        for coor in markers if markers != None else []:
            coor = coor["coordinates"]
            init_coords.append( [x, coor[0], coor[1]] )
            x = x + 1

    errors = {}
    if request.method == "POST":
        instance_form = InstanceForm(request.POST, instance=inst)

        if instance_form.is_valid():

            try:
                instance = instance_form.save()
            except Exception, err:
            	#transaction.rollback()
                log.error("error while saving instance: %s" % str(err))
                errors.update({"Updating instance": "Server error took place. Please contact the admin."})
            else:
            	#transaction.commit()
                return HttpResponseRedirect(reverse("admin:admin-base"))
        else:
            for f in instance_form.inner_trans_forms:
                if f.errors:
                    errors.update(f.errors)
            if instance_form.errors:
                errors.update(instance_form.errors)
    else:
        instance_form = InstanceForm(instance=inst)


    context = {
            'instance_form': instance_form,
            "init_coords": init_coords,
            'new': is_new,
            'errors': errors,
    }
    return render_to_response(template, RequestContext(request, context))

@login_required
def new(request, template="admin/trans_instance_edit.html"):
    return instance(request)

@login_required
def delete(request, instance_id, template="admin/trans_instance_del.html"):
    log.debug('deleting instance %s' % instance_id)
    is_new = False
    ok = verify(request)
    if ok != None:
        return ok

    try:
        inst = Instance.objects.untranslated().get(pk=instance_id)
    except Instance.DoesNotExist:
        raise Http404 ("instance with id %s does not exist" % instance_id)

    if request.method == "POST" and request.POST.has_key("submit_btn") and request.POST["submit_btn"] == "Confirm Delete?":
        inst.delete()
        return HttpResponseRedirect(reverse("admin:admin-base"))

    context = {
            'inst': inst,
    }
    log.debug('rendering %s' % template )
    return render_to_response(template, RequestContext(request, context))
