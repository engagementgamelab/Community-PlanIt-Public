from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from web.core.views import LoginRequiredMixin
from web.accounts.mixins import PlayerMissionStateContextMixin, MissionContextMixin
from web.accounts.models import PlayerMissionState
from .models import Cause
from .forms import CauseForm

class CauseListView(LoginRequiredMixin, PlayerMissionStateContextMixin, MissionContextMixin, ListView):
    model = Cause
    template_name = 'causes/bank.html'
    context_object_name = 'causes'


cause_list_view = CauseListView.as_view()


class CauseGameDetailView(LoginRequiredMixin, MissionContextMixin, DetailView):
    model = Cause
    template_name = 'causes/cause_game.html'
    pk_url_kwarg = 'id'
    context_object_name = 'cause'

cause_game_detail_view = CauseGameDetailView.as_view()


class CausePublicDetailView(DetailView):
    model = Cause
    template_name = 'causes/cause_public.html'
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

