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

@stringfilter
@register.filter
def languages_formatted(languages):
    return ", ".join(list(languages.values_list('name', flat=True)))

