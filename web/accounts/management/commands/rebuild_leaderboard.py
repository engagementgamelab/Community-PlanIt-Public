from django.core.management.base import BaseCommand

from web.instances.models import Instance
from web.instances.utils import leaderboard_for_game

import logging
log = logging.getLogger(__name__)

class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):

        current_games = Instance.objects.current()
        for game in current_games:
            leaderboard_for_game.invalidate(game)
            leaderboard_for_game(game)
            log.debug("rebuild leaderboard for %s" % game)


