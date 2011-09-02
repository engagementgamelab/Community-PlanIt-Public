from django.conf import settings
from django.template.defaultfilters import stringfilter
from django import template

register = template.Library()

@stringfilter
@register.filter
def lang(l):
    try:
        return dict(settings.LANGUAGES)[l]
    except:
        return "Unknown"
