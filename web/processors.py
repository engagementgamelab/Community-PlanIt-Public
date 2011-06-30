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
    try:
        profile = request.user.get_profile()
        instance = profile.instance
        missions = Mission.objects.filter(instance=instance)
        challenges = Challenge.objects.filter(instance=instance).active()
        
        # Filter out challenges that have already been accepted or played.
        player_challenges = PlayerChallenge.objects.filter(player=request.user).filter(challenge__start_date__lt=datetime.datetime.now()).filter(challenge__end_date__gt=datetime.datetime.now()).order_by('challenge__end_date')
        
        for player_challenge in player_challenges:
            challenges = challenges.exclude(id=player_challenge.challenge.id)
    
        finished_activities = Answer.objects.filter(answerUser=request.user)
        activities = []
        
        for fa in finished_activities:
            activities.append(fa.activity)
        return {
            'instance': instance,
            'missions': missions,
            'challenges': challenges,
            'player_challenges': player_challenges,
            'finished_activities': activities,
        }
    except: return {}
