import datetime
from web.missions.models import Mission
from web.reports.actions import ActivityLogger, PointsAssigner
from web.challenges.models import Challenge, PlayerChallenge
from web.player_activities.models import PlayerActivity
from web.answers.models import Answer

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
        
        #TODO: This was breaking hard, users would get 99 points and something would fail. The number of missions was 0,
        # the number of instances was 0, so it never got past this point. No errors were thrown in debug mode which 
        # terrifies me. -BMH
        # Calculate if any points have been awarded and not accounted for
        # to get coins.
        #offset = profile.points_multiplier or 1
        #if profile.points >= offset * 99:
        #    new_coins = math.floor(profile.points / (offset * 99))
        #    profile.coins += new_coins
        #    profile.points_multiplier = offset + new_coins
        #    profile.save()

        #    if new_coins > 1:
        #        ActivityLogger.log(request.user, request, 'to gain '+ str(new_coins) +' coins', 'earned over '+ str((profile.points_multiplier - 1) * 99) +' points', '/player/'+ str(request.user.id), 'coin')
        #    else:
        #        ActivityLogger.log(request.user, request, 'to gain a coin', 'earned over '+ str((profile.points_multiplier - 1) * 99) +' points', '/player/'+ str(request.user.id), 'coin')

        finished_activities = Answer.object.filter(user=request.user)
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
