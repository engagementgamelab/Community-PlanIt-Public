import time

import uwsgi
from .uwsgidecorators import spool, timer, cron

from django.core import management
from django.conf import settings
from django.utils import autoreload

@timer(3)
def change_code_gracefull_reload(sig):
    if autoreload.code_changed():
        uwsgi.reload()

#@timer(settings.REBUILD_LEADERBOARD_SLEEP_SECONDS, target='spooler')
#def rebuild_leaderboards(signum):
#    management.call_command('rebuild_leaderboards', interactivity=False)

#@timer(settings.CRON_MAIL_SLEEP_SECONDS, target='spooler')
#def django_mailer_send_mail(signum):
#    management.call_command('send_mail', interactivity=False)

#@timer(settings.CRON_MAIL_RETRY_DEFERRED_SLEEP_SECONDS, target='spooler')
#def django_mailer_retry_deferred(signum):
#    management.call_command('retry_deferred', interactivity=False)


#try:
#    from uwsgidecorators import spool
#except ImportError:
#    def spool(f):
#        f.spool = f
#        return f

@spool
def run_attachment_checks(arguments):
    # need to give some time for the attachment to be saved
    time.sleep(10)
    management.call_command('attachment_checks', attachment_id=arguments.get('attachment_id'), interactivity=False)

@spool
def uwsgi_assign_challenge_completed_badges(arguments):
    from web.badges.utils import assign_challenge_completed_badges
    assign_challenge_completed_badges(arguments.get('user_id'), arguments.get('mission_id'))

@spool
def uwsgi_run_report(arguments):
    from web.reporting.reports import (
                DemographicReport,
                LoginActivityReport,
                ChallengeActivityReport,
                MissionReport
    )
    reports = {
            'demographic': DemographicReport,
            'login-activity': LoginActivityReport,
            'challenge-activity': ChallengeActivityReport,
            'mission': MissionReport,
    }
    d = reports.get(arguments.get('report_name'))()
    kwargs={'instance_id' : arguments.get('instance_id')}
    d.run(**kwargs)

#@cron(59, 3, -1, -1, -1)
#def execute_me_at_three_and_fiftynine(num):
#    print("it's 3:59 in the morning")

@cron(50, 16, -1, -1, -1)
def run_reports(num):
    from web.reporting.reports import (
                DemographicReport,
                LoginActivityReport,
                ChallengeActivityReport,
                MissionReport
    )
    reports = {
            'demographic': DemographicReport,
            'login-activity': LoginActivityReport,
            'challenge-activity': ChallengeActivityReport,
            'mission': MissionReport,
    }
    d = reports.get('demographic')()
    kwargs={'instance_id' : '80'}
    d.run(**kwargs)

