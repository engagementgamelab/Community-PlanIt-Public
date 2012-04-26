from django import template

register = template.Library()

@register.inclusion_tag('accounts/_avatar.html')
def avatar(user):
    return {'user': user}
    
