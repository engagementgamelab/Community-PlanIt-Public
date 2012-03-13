from django.contrib.sites.models import RequestSite

from web.instances.models import Instance

import logging
log = logging.getLogger(__name__)

def instance_from_request(request):
    instance = None
    if request.user.is_authenticated():
        user_profile = request.user.get_profile()
        domain = RequestSite(request)
        try:
            instance = Instance.objects.get(for_city__domain=domain)
        except Instance.DoesNotExist:
            pass
    log.debug('user: %s,  current_instance: %s' % (str(request.user), str(instance)))
    return {
            'instance' : instance,
    }


