from django import template
from web.accounts.models import UserProfilePerInstance

register = template.Library()

@register.inclusion_tag('accounts/_game_nav.html', takes_context=True)
def game_nav(context):

    req =  context['request']
    user = req.user
    ctx = {}

    if user.is_authenticated() and req.session.has_key('my_active_game'):
        my_active_game = req.session.get('my_active_game')
        profile = user.get_profile()
        screen_name = profile.screen_name
        ctx.update({
            'screen_name': screen_name,
            'player_id': user.pk,
            'my_active_game': my_active_game,
            'my_active_game_profile': UserProfilePerInstance.objects.\
                                            get(user_profile=profile,
                                                instance=my_active_game),

            'my_non_active_game_profiles': UserProfilePerInstance.objects.\
                        filter(user_profile=profile).\
                        exclude(instance=my_active_game)
        })
    print ctx
    return ctx
    
