import time

import uwsgi
from .uwsgidecorators import spool, timer

from django.core import management
from django.conf import settings
from django.utils import autoreload

#@timer(3)
#def change_code_gracefull_reload(sig):
#    if autoreload.code_changed():
#        uwsgi.reload()

@spool
def run_attachment_checks(arguments):
    # need to give some time for the attachment to be saved
    time.sleep(10)
    management.call_command('attachment_checks', attachment_id=arguments.get('attachment_id'), interactivity=False)


@timer(settings.REBUILD_LEADERBOARD_SLEEP_SECONDS, target='spooler')
def rebuild_leaderboards(signum):
    management.call_command('rebuild_leaderboards', interactivity=False)

