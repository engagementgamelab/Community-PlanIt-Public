import time

import uwsgi
from .uwsgidecorators import spool, timer, cron

from django.core import management
from django.conf import settings
from django.utils import autoreload

#@timer(3)
#def change_code_gracefull_reload(sig):
#    if autoreload.code_changed():
#        uwsgi.reload()

@cron(30, -1, -1, -1, -1)
def rebuild_leaderboards(signum):
    if settings.DEBUG == False:
        management.call_command('rebuild_leaderboards', interactivity=False)

@cron(2, -1, -1, -1, -1)
def django_mailer_send_mail(signum):
    if settings.DEBUG == False:
        management.call_command('send_mail', interactivity=False)

@cron(20, -1, -1, -1, -1)
def django_mailer_retry_deferred(signum):
    if settings.DEBUG == False:
        management.call_command('retry_deferred', interactivity=False)

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

@cron(0, 6, -1, -1, -1)
def daily_email_digest(num):
    if settings.DEBUG == False:
        management.call_command('daily_email_digest', interactivity=False)

@cron(0, 2, -1, -1, -1)
def run_reports(num):
    if settings.DEBUG == False:
        management.call_command('run_reports', interactivity=False)
