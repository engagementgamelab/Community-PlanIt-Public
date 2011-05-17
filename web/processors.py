import datetime
from web.missions.models import Mission
from web.reports.actions import ActivityLogger, PointsAssigner
from web.challenges.models import Challenge, PlayerChallenge
from web.games.models import Game, PlayerGame

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

        # Calculate if any points have been awarded and not accounted for
        # to get coins.
        offset = profile.points_multiplier or 1
        if profile.points >= offset * 99:
            new_coins = math.floor(profile.points / (offset * 99))
            profile.coins += new_coins
            profile.points_multiplier = offset + new_coins
            profile.save()

            if new_coins > 1:
                ActivityLogger.log(request.user, request, 'to gain '+ str(new_coins) +' coins', 'earned over '+ str((profile.points_multiplier - 1) * 99) +' points', '/player/'+ str(request.user.id), 'coin')
            else:
                ActivityLogger.log(request.user, request, 'to gain a coin', 'earned over '+ str((profile.points_multiplier - 1) * 99) +' points', '/player/'+ str(request.user.id), 'coin')

        player_games = PlayerGame.objects.filter(visible=True, completed=True, user=request.user)
        games = []
        for pg in player_games:
            games.append(pg.game)

        return {
            'instance': instance,
            'missions': missions,
            'challenges': challenges,
            'player_challenges': player_challenges,
            'games': games,
        }
    except: return {}
