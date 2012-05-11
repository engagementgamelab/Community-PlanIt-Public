from django import template
from web.settings import HEATMAP_THRESHOLD
register = template.Library()

@register.filter
def heatmap(value):
    '''
        Used to filter comments "hotness" by count. 0-2, 3-5, 6-8, 9-11, 12-14, 15-17.
        Anything more than 25 should just be very hot.
    '''
    quotient = value/HEATMAP_THRESHOLD
    if quotient > 5:
        return 5
    else:
        return quotient
