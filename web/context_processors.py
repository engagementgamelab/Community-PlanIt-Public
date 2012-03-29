from django.contrib.sites.models import RequestSite

from web.instances.models import Instance

#from web.core.utils import instance_from_request as utils_instance_from_request 

import logging
log = logging.getLogger(__name__)

#def instance_from_request(request):
#    instance = None
#    if request and request.user.is_authenticated():
#        instance = utils_instance_from_request(request)
#        log.debug('city %s, user: %s,  current_instance: %s' % (instance.for_city.domain, str(request.user), str(instance)))
#    return { 'instance' : instance, }


