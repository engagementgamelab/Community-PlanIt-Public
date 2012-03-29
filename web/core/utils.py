from nani.utils import get_translation

from django.conf import settings
from django.utils.translation import get_language
from django.contrib.sites.models import RequestSite

from instances.models import Instance

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
