from .models import Cause, PlayerCauseTransaction


class CausesContextMixin(object):
    """ insert coins counts into Bank context """

    def get_context_data(self, *args, **kwargs):
        ctx = super(CausesContextMixin, self).get_context_data(*args, **kwargs)
        return ctx

