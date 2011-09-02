from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.db.models import get_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404

import logging
log = logging.getLogger(__name__)

def verify(request, template="admin/backend_not_superuser.html"):
    user = request.user
    if user.is_superuser:
        return None
    else:
        return render_to_response(template, RequestContext(request, context))

@login_required
def delete_obj(request, id, model, template="admin/trans_del.html"):
    is_new = False
    ok = verify(request)
    if ok != None:
        return ok

    app, klass = model.split('.')
    model_klass = get_model(app, klass)

    try:
        inst = model_klass.objects.untranslated().get(pk=id)
    except model_klass.DoesNotExist:
        raise Http404 ("%s with id %s does not exist" % (model_klass.__name__, id))

    if model == "values.Value":
        redir = reverse("admin:manage-values", args=(id,))
    else:
        redir = reverse("admin:admin-base")


    if request.method == "POST" and request.POST.has_key("submit_btn") and request.POST["submit_btn"] == "Confirm Delete?":
        inst.delete()
        return HttpResponseRedirect(redir)

    context = {
            'inst_formatted': model_klass.__name__,
            'redir_cancel': redir,
    }
    log.debug('rendering %s' % template )
    return render_to_response(template, RequestContext(request, context))
