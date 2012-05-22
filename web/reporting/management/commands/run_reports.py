from django.core.management.base import BaseCommand, CommandError
from optparse import make_option

from django.conf import settings
from web.instances.models import Instance

from web.reporting.reports import (
            DemographicReport,
            LoginActivityReport,
            ChallengeActivityReport,
            MissionReport
)
import logging
log = logging.getLogger(__name__)

class Command(BaseCommand):
    option_list = BaseCommand.option_list +(
            make_option('--game_id', '-g', action='store', dest='game_id', default=None, help='Game [primary key] to run reports on.'),
    )
    help = 'Trigger creation of reports.'

    def handle(self, *args, **options):
        #log.debug("coll_command args: %s" % args)
        if len(args) > 1:
            raise CommandError("extra arguments supplied")

        game_id = options['game_id']

        current_games = Instance.objects.current()
        for report_class in (
                            DemographicReport,
                            LoginActivityReport,
                            ChallengeActivityReport,
                            #MissionReport,
                            ):

            if game_id:
                rpt = report_class(instance_id=game_id)
                rpt.run()
            else:
                for game in current_games:
                    rpt = report_class(instance_id=game.pk)
                    rpt.run()
