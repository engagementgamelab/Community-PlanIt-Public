from django.contrib.sites.models import RequestSite

from web.instances.models import Instance

def instance_from_request(request):
    user_profile = request.user.get_profile()
    domain = RequestSite(request)
    try:
        instance = Instance.objects.get(for_city__domain=domain)
    except Instance.DoesNotExist:
        pass
    return {
            'instance' : instance,
    }


