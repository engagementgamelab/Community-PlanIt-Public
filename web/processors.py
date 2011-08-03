import datetime
from web.missions.models import Mission
from web.reports.actions import ActivityLogger, PointsAssigner
from web.challenges.models import Challenge, PlayerChallenge
from web.player_activities.models import PlayerActivity
from web.answers.models import Answer
from web.instances.models import Instance
# Provides "globals" within the templates to populate things such as the sidebar
# and other content that was previously only generated in the dashboard.
def instance_processor(request):
    if request.user.is_anonymous():
        return {}

    instance = request.user.get_profile().instance
    if not instance:
        if request.user.is_staff or request.user.is_superuser:
            instance = Instance.objects.active().latest()

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
