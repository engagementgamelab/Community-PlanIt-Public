from attachments.models import Attachment


class ChallengeContextMixin(object):
    """ Context for a challenge. Create or Detail views """

    def get_context_data(self, *args, **kwargs):
        context = super(ChallengeContextMixin, self).get_context_data(*args, **kwargs)
        # attachments are inserted into the context using the
        # attachments_tags
        context['challenge_resources'] = Attachment.objects.filter(parent=self.challenge)
        return context
