from django import template
from sorl.thumbnail.parsers import parse_geometry

register = template.Library()

@register.inclusion_tag('accounts/_avatar.html')
def avatar(user, geometry):

    return {
    	'user': user,
    	'geometry': geometry,
    	'geometry_width': parse_geometry(geometry)[0],
    	'geometry_height': parse_geometry(geometry)[1],
    }