import datetime
from django.core.management.base import BaseCommand

from web.instances.models import Instance
from web.core.utils import leaderboard_for_game

import logging
log = logging.getLogger(__name__)

class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):

        current_games = Instance.objects.current()
        for game in current_games:
            leaderboard_for_game.invalidate(game)
            log.debug("rebuild leaderboard for %s" % game)
            t1 = datetime.datetime()
            leaderboard_for_game(game)
            t2 = datetime.datetime()
            log.debug("done rebuild leaderboard for %s in %s" % (game, str(t2-t1)))


