from django.contrib.sites.models import RequestSite

from web.instances.models import Instance
from web.accounts.models import UserProfilePerInstance

import logging
log = logging.getLogger(__name__)

def game_nav(request):
    ctx = {}
    if request.user.is_authenticated() and \
                    request.session.has_key('my_active_game'):
        ctx.update({
            'my_non_active_game_profiles': UserProfilePerInstance.objects.\
                        filter(user_profile=request.user.get_profile()).\
                        exclude(instance=request.session.get('my_active_game'))
        })
    return ctx
