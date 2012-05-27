import time 
from django.core.management.base import BaseCommand
from django.db import connection

from web.instances.models import Instance
from web.core.utils import leaderboard_for_game

import logging
log = logging.getLogger(__name__)

class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        current_games = Instance.objects.current()
        for game in current_games:
            leaderboard_for_game.invalidate(game.pk)
            t1 = time.time()
            leaderboard_for_game(game.pk)
            t2 = time.time()
            log.debug("done rebuilding leaderboards for %s in %s min. %s queries." % (game, (time.time()-t1)/60, len(connection.queries)))

