from web.challenges.models import Challenge, PlayerChallenge
from web.instances.models import Instance
from web.player_activities.models import PlayerActivity
#from web.core.utils import _fake_latest

# Provides "globals" within the templates to populate things such as the sidebar
# and other content that was previously only generated in the dashboard.
#
# TODO: this should be eliminated in favor of explicitly supplying the info
# to templates that need it; having variables magically appear in the template
# context, possibly conflicting with context variables from the view, can be
# problematic. There are also cases where users may not have profiles or be
# associated with an instance (non-participatory admin users); they require
# extra care here to avoid exceptions. JH
def instance_processor(request):
    if request.user.is_anonymous():
        return {}

    instance = request.user.get_profile().instance
    if not instance:
        if request.user.is_staff or request.user.is_superuser:
            instances = Instance.objects.untranslated()
            if instances.count():
                instance = instances.latest()
                #instance = _fake_latest(Instance, Instance.objects.untranslated())

    if not instance:
        return {}

    missions = instance.missions.all()
    challenges = instance.challenges.available(request.user)
    player_challenges = PlayerChallenge.objects.filter(challenge__instance=instance).available().order_by('challenge__end_date')
    
    finished_activities = PlayerActivity.objects.filter(answers__answerUser=request.user)

    return {
        'instance': instance,
        'missions': missions,
        'challenges': challenges,
        'player_challenges': player_challenges,
        'finished_activities': finished_activities,
    }
