from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from web.core.views import LoginRequiredMixin
from web.values.models import Value

class CauseListView(LoginRequiredMixin, ListView):
    model = Value
    template_name = 'causes/bank.html'
    context_object_name = 'causes'

    def get_context_data(self, **kwargs):
        context = super(CauseListView, self).get_context_data(**kwargs)

        return context

cause_list_view = CauseListView.as_view()


class CauseGameDetailView(LoginRequiredMixin, DetailView):
    model = Value
    template_name = 'causes/cause_game.html'
    pk_url_kwarg = 'id'
    context_object_name = 'cause'


cause_game_detail_view = CauseGameDetailView.as_view()

class CausePublicDetailView(DetailView):
    model = Value
    template_name = 'causes/cause_public.html'
    pk_url_kwarg = 'id'
    context_object_name = 'cause'

cause_public_detail_view = CausePublicDetailView.as_view()