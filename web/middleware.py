from django.contrib.sites.models import RequestSite
from django.utils.translation import get_language
from web.instances.models import Instance, City

class CurrentDomainMiddleware(object):

    def process_request(self, request):
        if not request.is_ajax():
            request.current_site = RequestSite(request)
            
            try:
                current_city = City.objects.get(domain=request.current_site)
            except City.DoesNotExist:
                current_city = None
            request.current_city = current_city
            
            if request.session.has_key('current_game_slug') and \
                    not hasattr(request, 'current_game'):
                request.current_game = Instance.objects.language(get_language()).get(
                            slug=request.session.get('current_game_slug')
                )
        return None
