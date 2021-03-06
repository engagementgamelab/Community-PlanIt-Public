from django.shortcuts import redirect, get_object_or_404
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from web.core.views import LoginRequiredMixin
from web.instances.models import Instance
from web.accounts.mixins import PlayerMissionStateContextMixin, MissionContextMixin
from web.accounts.models import PlayerMissionState
from .models import Cause
from .forms import CauseForm
from .mixins import CausesContextMixin

class CauseListView(LoginRequiredMixin,
                    #PlayerMissionStateContextMixin,
                    MissionContextMixin,
                    ListView):
    model = Cause
    template_name = 'causes/cause_list.html'
    context_object_name = 'causes'


cause_list_view = CauseListView.as_view()



class BankContextMixin(object):
    """ gather context for the bank"""

    def get_context_data(self, *args, **kwargs):
        context = super(MissionContextMixin, self).get_context_data(*args, **kwargs)
        active_game = self.request.session.get('my_active_game', None)

        return context

class CauseGameDetailView(LoginRequiredMixin, MissionContextMixin, DetailView):
    model = Cause
    template_name = 'causes/cause_detail_game.html'
    pk_url_kwarg = 'id'
    context_object_name = 'cause'

cause_game_detail_view = CauseGameDetailView.as_view()


class CausePublicDetailView(DetailView):
    model = Cause
    template_name = 'causes/cause_detail_public.html'
    pk_url_kwarg = 'id'
    context_object_name = 'cause'

cause_public_detail_view = CausePublicDetailView.as_view()


class CauseCreateView(MissionContextMixin, CreateView):
    form_class = CauseForm
    template_name = "causes/cause_create.html"
    context_object_name = 'cause'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.creator = self.request.user
        self.object.instance = self.request.session.get('my_active_game', None)
        self.object.save()
        messages.success(self.request, _("You've created a cause. Wait until moderators approve it."))
        return redirect(reverse('instances:causes:bank', args=(self.object.instance.slug,)))

cause_add_view = CauseCreateView.as_view()

class SponsorListView(MissionContextMixin, TemplateView):
    template_name = 'causes/sponsor_list.html'

sponsor_list_view = SponsorListView.as_view()

class CoinsView(LoginRequiredMixin, MissionContextMixin, CausesContextMixin, TemplateView):
    template_name = 'causes/coins.html'

    def dispatch(self, request, *args, **kwargs):
        self.game = get_object_or_404(Instance, slug=kwargs['game_slug'])
        return super(CoinsView, self).dispatch(request, *args, **kwargs)

coins_view = CoinsView.as_view()
