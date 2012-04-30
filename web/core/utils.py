from nani.utils import get_translation

from django.conf import settings
from django.utils.translation import get_language
from django.contrib.sites.models import RequestSite

from web.instances.models import Instance
from web.missions.models import Mission

import logging
log = logging.getLogger(__name__)

def _fake_latest(model, qs):
    if model and qs:
        _get_latest_by = model._meta.get_latest_by
        _latest_by = max(qs.values_list(_get_latest_by, flat=True))
        return model.objects.get(**{_get_latest_by:_latest_by})

def get_translation_with_fallback(obj, attr):
    if not get_language() in obj.get_available_languages():
        trans_model = obj.__class__.objects.translations_model()
        try:
            return getattr(get_translation(obj, settings.LANGUAGE_CODE), attr)
        except trans_model.DoesNotExist:
            return "---"
    return getattr(obj, attr)

def instance_from_request(request):
    #user_profile = request.user.get_profile()
    domain = RequestSite(request)
    try:
        return Instance.objects.get(for_city__domain=domain)
    except Instance.DoesNotExist:
        return

def missions_bar_context(request, mission=None):
    if not mission:
        mission = Mission.objects.default(instance=request.current_game)

    my_points_for_mission, progress_percentage = request.prof_per_instance.progress_percentage_by_mission(mission)
    all_missions_for_game = Mission.objects.filter(instance=request.current_game)
    my_flags_count = request.prof_per_instance.flags
    log.debug("i have %s flags" % my_flags_count)
    my_flags_range = range(0, my_flags_count)

    context = {
        'mission': mission,
        'all_missions_for_game': all_missions_for_game,
        'my_points_for_mission': my_points_for_mission,
        'progress_percentage': progress_percentage,
        'my_flags_range': my_flags_range,
    }

    return context




