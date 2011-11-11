from django.core.management.base import BaseCommand
from stream import utils as stream_utils
from stream.models import Action
from reports.models import Activity
from challenges.models import Challenge, PlayerChallenge

class Command(BaseCommand):
    help = "populate django-stream `Action` objects from db."

    def handle(self, *args, **options):

        def register_reply(comment, parent_comment):
            Action.objects.create(
                    actor=comment.user,
                    verb='replied',
                    action_object=comment, 
                    target=parent_comment,
                    datetime=comment.posted_date,
                    description="replied with a comment"
            )
            print "ran 'replied'"
            for c in comment.comments.all():
                register_reply(c, comment)

        for pc in PlayerChallenge.objects.filter():
            for comment in pc.comments.all():
                Action.objects.create(
                            actor=comment.user,
                            verb='challenge_commented',
                            action_object=comment, 
                            target=pc,
                            datetime=comment.posted_date,
                            description="comment on a challenge"
                )
                print "ran 'challenge_commented'"
                for u in comment.likes.all():
                    Action.objects.create(
                            actor=u,
                            verb='liked',
                            target=comment,
                            datetime=comment.posted_date,
                            description="liked a comment"
                    )
                    print "ran 'liked'"
                for c in comment.comments.all():
                    register_reply(c, comment)

        return

        qs = Activity.objects.filter(action__icontains='challenge')
        d = {
                'created': ('challenge_created', 'a challenge was created'),
                'completed': ('challenge_completed', 'a challenge was completed'),
        }
        for activity in qs.filter(data__in=['completed', 'created']):
            url = activity.url[-3:-1] if activity.url.endswith('/') else activity.url[-2:]
            try:
                challenge = Challenge.objects.get(pk=url)
            except Challenge.DoesNotExist:
                print vars(activity)
            else:
                verb, description = d.get(activity.data)
                Action.objects.create(
                                actor=activity.user,
                                verb=verb,
                                target=activity.instance,
                                action_object=challenge,
                                datetime=activity.date,
                                description=description,
                )




