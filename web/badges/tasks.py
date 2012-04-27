from celery.task import Task, task
from celery.registry import tasks

import logging
log = logging.getLogger(__name__)

@task
def add(x,y):
	return x+y

class TestT(Task):
    def run(self, *args, **kwargs):
        test_id = self.request.kwargs.get('test_id')
        print("executed task id: %r, test_id: %r " %(self.request.id, test_id))
tasks.register(TestT)
