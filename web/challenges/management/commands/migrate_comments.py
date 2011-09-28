from django.core.management.base import BaseCommand
from challenges.models import PlayerChallenge

class Command(BaseCommand):
    help = "My shiny new management command."

    def handle(self, *args, **options):
        challenges = PlayerChallenge.objects.all()
        print "got %s challenges " % challenges.count()
        for pc in challenges:
            #import ipdb;ipdb.set_trace()
            if pc.response.message != '':
                print "processing %s ..." % pc.response.message[:10]
                comment = pc.comments.create(
                    content_object=pc,
                    message=pc.response.message,
                    user=pc.player,
                    instance=pc.challenge.instance,
                )
                for att in pc.attachments.all():
                    if att.url is not None:
                        comment.attachment.create(
                                file=None,
                                url=att.url,
                                type='video',
                                user=pc.player,
                                instance=pc.challenge.instance,
                        )
                    else:
                        comment.attachment.create(
                                file=att.file,
                                type='image',
                                user=pc.player,
                                instance=pc.challenge.instance,
                        )

