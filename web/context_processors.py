from django.contrib.sites.models import RequestSite

from web.instances.models import Instance

import logging
log = logging.getLogger(__name__)

def instance_from_request(request):
    domain = instance = None
    if request.user.is_authenticated():
        user_profile = request.user.get_profile()
        domain = RequestSite(request)
        try:
            instance = Instance.objects.get(for_city__domain=domain)
        except Instance.DoesNotExist:
            pass

    if domain is not None:
        domain_name = domain.domain
    else:
        domain_name='-none-'

    log.debug('domain: %s, user: %s,  current_instance: %s' % (domain_name, str(request.user), str(instance)))
    return {
            'instance' : instance,
    }


