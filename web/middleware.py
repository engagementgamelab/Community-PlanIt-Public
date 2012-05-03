from django.http import Http404
from django.contrib.sites.models import RequestSite
from django.utils.translation import get_language
from web.instances.models import Instance, City
from web.accounts.models import UserProfilePerInstance

import logging
log = logging.getLogger(__name__)


class CurrentDomainMiddleware(object):
    def process_request(self, request):
        #log.debug("middleware. auth?: %s" % request.user.is_authenticated())

        request.current_site = RequestSite(request)
        try:
            current_city = City.objects.for_domain(domain=request.current_site)
        except City.DoesNotExist:
            current_city = None
        request.current_city = current_city


        if request.session.has_key('current_game_slug') and \
                not hasattr(request, 'current_game'):
            #request.current_game = Instance.objects.language(get_language()).for_slug(
            #            slug=request.session.get('current_game_slug')
            #)
            request.current_game = Instance.objects.for_slug(
                        slug=request.session.get('current_game_slug')
            )
            try:
                prof_per_instance = UserProfilePerInstance.objects.get(
                            instance=request.current_game, 
                            user_profile=request.user.get_profile()
                )
            except UserProfilePerInstance.DoesNotExist:
                raise Http404("user for this game is not registered")

            request.prof_per_instance  = prof_per_instance 
            #request.my_total_points = prof_per_instance.total_points
            #request.my_flags_count = prof_per_instance.flags
        return None
