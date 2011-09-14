import os
import subprocess
import sys
from optparse import make_option

from django.core.management.base import BaseCommand
from django.db import connections, router, transaction, DEFAULT_DB_ALIAS

class Command(BaseCommand):
    help = 'Installs the named fixture(s) in the database, replacing all occurrences of {{INSTANCE_ID}} with the supplied instance ID. Supply the full path to each fixture template.'
    args = "instance_id fixture_template [fixture_template ...]"

    option_list = BaseCommand.option_list + (
        make_option('--database', action='store', dest='database',
            default=DEFAULT_DB_ALIAS, help='Nominates a specific database to load '
                'fixtures into. Defaults to the "default" database.'),
    )

    def handle(self, *args, **options):

        if len(args) > 0:
            instance_id = args[0]
        else:
            self.print_help(sys.argv[0], 'loadinstancedata')
            sys.exit(1)

        if len(args) > 1:
            fixtures = []
            for datafile_template in args[1:]:
                template = open(datafile_template)
                fixture_filename = "%s/%s_%s" % (os.path.dirname(datafile_template), instance_id, os.path.basename(datafile_template))
                fixture = open(fixture_filename, 'w')
                for line in template:
                    fixture.write(line.replace('{{INSTANCE_ID}}', instance_id))
                fixture.close()
                fixtures.append(fixture_filename)

            command = [sys.argv[0], 'loaddata']
            for option, value in options.items():
                if value:
                    command.append('--%s=%s' % (option, value))

            for fixture in fixtures:
                command.append(os.path.splitext(os.path.basename(fixture))[0])

            subprocess.Popen(command, stdin=None, stdout=None, stderr=None).wait()
        else:
            self.print_help(sys.argv[0], 'loadinstancedata')
            sys.exit(1)
