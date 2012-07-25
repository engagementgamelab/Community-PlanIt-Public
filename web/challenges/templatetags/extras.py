from django import template

register = template.Library()

@register.filter(name="subtractFrom")
def subtractFrom(value, sub):
    try:
        return int(sub) - int(value)
    except TypeError:
        return value
    