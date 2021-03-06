from nani.utils import get_translation

from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
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

    try:
        instance = Instance.objects.untranslated().get(pk=int(instance_id))
    except Instance.DoesNotExist:
        raise Http404 ("Instance with id %s does not exist" % instance_id)

    if (request.POST.has_key("submit_btn") and request.POST["submit_btn"] == "Cancel"):
        return HttpResponseRedirect(reverse("admin:manage-values", args=[instance_id]))

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

    log.debug("value_id: %s" % value_id)
    log.debug("instance_id: %s" % instance_id)

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
        value = Value.objects.create(instance=instance, commit=False)
        is_new = True

    errors = {}
    form = ValueForm(instance=value, languages=instance.languages.all(), data=request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            try:
                value = form.save(commit=True)
            except Exception, err:
                #transaction.rollback()
                log.error("error while saving value: %s" % str(err))
                errors.update({"Updating value": "Server error took place. Please contact the admin."})
            else:
                #transaction.commit()
                return HttpResponseRedirect(reverse("admin:manage-values", args=[instance_id]))
        else:
            for f in form.inner_trans_forms:
                if f.errors:
                    errors.update(f.errors)
            if form.errors:
                errors.update(form.errors)

    context = {
            'value': value,
            'instance': instance,
            'value_form': form,
            'new': is_new,
            'errors': errors,
    }

    return render_to_response(template, RequestContext(request, context))


#@login_required
#def delete(request, instance_id, value_id, model, template="admin/trans_instance_del.html"):
#	return delete_obj(request)

