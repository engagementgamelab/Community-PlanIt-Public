from nani.utils import get_translation

from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

from instances.models import Instance
from values.models import Value
from admin.views import verify
from admin.forms import ValueForm

import logging
log = logging.getLogger(__name__)

def trans_for_value(value):
    return [get_translation(value, lang) for lang in instance.get_available_languages()],

@login_required
def manage(request, instance_id, template="admin/manage_values.html"):
    ok = verify(request)
    if ok != None:
        return ok
    #TODO: Make the instances only be drawn from instances that the user supervises

    try:
        instance = Instance.objects.untranslated().get(pk=int(instance_id))
    except Instance.DoesNotExist:
        raise Http404 ("Instance with id %s does not exist" % instance_id)

    data = {}
    for value in Value.objects.untranslated().filter(instance=instance):
        #Value.objects.untranslated().filter(instance=instance)
        data[value] = {
                'value_translations': value.translations.all(),
                #'value_translations': trans_for_value(value),
        }
    context = {
        'data' : data,
        'instance' : instance,
    }
    return render_to_response(template, RequestContext(request, context))


@login_required
def value(request, instance_id, value_id=None, template="admin/trans_value_edit_new.html"):
    is_new = False
    ok = verify(request)
    if ok != None:
        return ok

    try:
        instance = Instance.objects.untranslated().get(pk=int(instance_id))
    except Instance.DoesNotExist:
        raise Http404 ("Instance with id %s does not exist" % instance_id)

    if (request.POST.has_key("submit_btn") and request.POST["submit_btn"] == "Cancel"):
        return HttpResponseRedirect(reverse("admin:manage-values", args=[instance_id]))

    if value_id is not None and value_id != 'None':
        try:
            value = Value.objects.untranslated().get(pk=int(value_id))
        except Value.DoesNotExist:
            raise Http404 ("value with id %s does not exist" % value_id)
    else:
        value = None
        is_new = True

    errors = {}
    value_form = ValueForm(value_instance=instance, instance=value, data=request.POST or None)

    if request.method == "POST":
        if value_form.is_valid():
            try:
                value = value_form.save(commit=False)
            except Exception, err:
                #transaction.rollback()
                print "error while saving value: %s" % str(err)
                log.error("error while saving value: %s" % str(err))
                errors.update({"Updating value": "Server error took place. Please contact the admin."})
            else:
                #transaction.commit()
                return HttpResponseRedirect(reverse("admin:manage-values", args=[instance_id]))
        else:
            for f in value_form.inner_trans_forms:
                if f.errors:
                    errors.update(f.errors)
            if value_form.errors:
                errors.update(value_form.errors)

    context = {
            'value': value,
            'instance': instance,
            'value_form': value_form,
            'new': is_new,
            'errors': errors,
    }

    return render_to_response(template, RequestContext(request, context))


@login_required
def new(request, instance_id):
    return value(request, instance_id)

@login_required
def delete(request, value_id):
    pass



