from celery.task import Task, task
from celery.registry import tasks
from stream.models import Action

from django.contrib.auth.models import User

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


@task
def gen_badges(user_id, **kwargs):
    print user_id
    print kwargs
    user = User.objects.get(pk=user_id)
    comments_for_user = Action.objects.filter(actor_user=user, verb='commented').count()

    if comments_for_user > CommunityBuilderRules.COMMENTS_PER_LEVEL:
        badge = Badge.objects.get(type=Badge.BADGE_COMMUNITY_BUILDER)
        badge_per_player, created = BadgePerPlayer.objects.get_or_create(
                                        badge=badge,
                                        user=user
        )
        # calculate level
        badge_per_player.level = comments_for_user % CommunityBuilderRules.TOTAL_LEVELS

