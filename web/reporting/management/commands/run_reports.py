from django.core.management.base import BaseCommand, CommandError
from optparse import make_option

from web.reporting.reports import ReportHandler
import logging
log = logging.getLogger(__name__)

class Command(BaseCommand):
    option_list = BaseCommand.option_list +(
            make_option('--game_id', '-g', action='store', dest='game_id', default=None, help='Game [primary key] to run reports on.'),
    )
    help = 'Command to run reports on games'

    def handle(self, *args, **options):
        #log.debug("coll_command args: %s" % args)
        if len(args) > 1:
            raise CommandError("extra arguments supplied")

        h = ReportHandler(game_id=options['game_id'])
        h.run_reports()
