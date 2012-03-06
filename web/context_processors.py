from django.contrib.sites.models import RequestSite

from web.instances.models import Instance


def instance_from_request(request):
    domain = RequestSite(request)
    return {
            'latest_for_city_domain' : Instance.objects.latest_for_city_domain(domain),
    }


