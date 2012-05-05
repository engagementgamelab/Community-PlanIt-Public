from celery.task import Task, task
from celery.registry import tasks

from django.core import management

import logging
log = logging.getLogger(__name__)

@task
def run_attachment_checks(**kwargs):
    log.debug('running celery task to check video attachments')
    management.call_command('attachment_checks', interactivity=False)


