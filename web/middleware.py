from django.contrib.sites.models import RequestSite
from web.instances.models import Instance

class CurrentDomainMiddleware(object):

    def process_request(self, request):

        request.current_site = RequestSite(request)

        if request.session.has_key('current_game_slug') and \
                not hasattr(request, 'current_game'):
            request.current_game = Instance.objects.get(
                        slug=request.session.get('current_game_slug')
            )
        return None
