from django.core.management.base import BaseCommand
from stream import utils as stream_utils
from stream.models import Action
from reports.models import Activity
from challenges.models import Challenge, PlayerChallenge
from player_activities.models import PlayerMapActivity, PlayerEmpathyActivity, PlayerActivity
from values.models import Value

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

        def register_main():
            d = {
                'challenge' : {
                        'created': ('challenge_created', 'a challenge was created'),
                        'completed': ('challenge_completed', 'a challenge was completed'),
                }
                'activity' : {
                        'completed': ('activity_completed', 'an activity was completed'),
                        'replayed': ('activity_replayed', 'an activity was replayed'),
                }
                'value' : {
                        'token spent': ('token_spent', 'token was spent'),
                        'token reclaimed': ('token_reclaimed', 'token was reclaimed'),
                }
            }
            for activity in Activity.objects.filter(type__in=['challenge', 'activity', 'value']):
                if not (activity.data and activity.url):
                    print vars(activity)
                    continue

                url = ''
                if activity.url:
                    for i in activity.url.split('/'):
                        if i.isdigit():
                            url = i
                if not url:
                    print (activity.pk, url)

                if "empathy" in activity.url:
                    klass = PlayerEmpathyActivity
                elif "map" in activity.url:
                    klass = PlayerMapActivity
                elif "challenge" in activity.url:
                    klass = Challenge
                elif "values" in activity.url:
                    klass = Value
                else:
                    klass = PlayerActivity
                try:
                    obj = klass.objects.get(pk=url)
                except klass.DoesNotExist:
                    continue

                verb, description = d.get(activity.type).get(activity.data, (None, None))
                if verb and description:
                    Action.objects.create(
                        actor=activity.user,
                        verb=verb,
                        action_object=obj,
                        datetime=activity.date,
                        description=description,
                    )

        def register_activity_comments():

            def create_action(answers, activity):

                for answ in answers.select_related('comments').all():
                    for comment in answ.comments.select_related('user', 'selected', 'likes').all():
                        Action.objects.create(
                                    actor=comment.user,
                                    verb='commented',
                                    action_object=comment, 
                                    target=activity,
                                    datetime=comment.posted_date,
                                    description="comment on an activity"
                        )
                        #print "ran 'challenge_commented'"
                        for u in comment.likes.all():
                            Action.objects.create(
                                    actor=u,
                                    verb='liked',
                                    target=comment,
                                    datetime=comment.posted_date,
                                    description="liked a comment"
                            )
                            #print "ran 'liked'"
                        for c in comment.comments.all():
                            register_reply(c, comment)

            for a in PlayerEmpathyActivity.objects.select_related().all():
            	answers = getattr(a, 'empathy_answers')
                create_action(answers, a)

            for a in PlayerActivity.objects.select_related().all().order_by('type'):
                if a.type.type == 'open_ended':
                    answers = getattr(a, 'openended_answers')
                    create_action(answers, a)
                elif a.type.type == 'single_response':
                    answers = getattr(a, 'singleresponse_answers')
                    create_action(answers, a)

            for a in PlayerMapActivity.objects.select_related().all():
                answers = getattr(a, 'map_answers')
                create_action(answers, a)

        def register_challenge_comments():
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


        register_main()
        register_challenge_comments()
        register_activity_comments()



