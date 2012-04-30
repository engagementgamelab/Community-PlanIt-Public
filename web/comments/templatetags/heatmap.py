from django import template
from web.settings import HEATMAP_THRESHOLD
register = template.Library()

@register.filter
def heatmap(value):
    '''
        Used to filter comments "hotness" by count. 1-5, 6-10, 11-15, 16-20, 20-25.
        Anything more than 25 should just be very hot.
    '''
    quotient = value/HEATMAP_THRESHOLD
    if quotient > 5: # Only have
        return 5
    else:
        return quotient
