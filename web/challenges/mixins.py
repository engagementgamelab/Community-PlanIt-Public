from attachments.models import Attachment


class ChallengeContextMixin(object):
    """ Context for a challenge. Create or Detail views """

    def get_context_data(self, *args, **kwargs):
        context = super(ChallengeContextMixin, self).get_context_data(*args, **kwargs)
        context['attachments'] = Attachment.objects.attachments_for_object(self.challenge)
        return context
