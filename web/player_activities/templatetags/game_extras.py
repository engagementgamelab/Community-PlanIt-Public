from django import template

from web.instances.models import PointsAssignment
from web.player_activities.models import PlayerActivityBase

register = template.Library()

class GetPointsNode(template.Node):
    def __init__(self, action, var=None):
        self.action = action
        self.var = var

    def render(self, context):
        instance = context['instance']

        try:
            points_assignment = PointsAssignment.objects.get(instance=instance, action__action=self.action)
            points = points_assignment.points
        except:
            points = 0
        
        if self.var:
            context[self.var] = points
            return ''
        return points

@register.tag(name="get_points")
def do_get_points(parser, token):
    """
      usage: {% get_points challenge_created %}
      usage: {% get_points challenge_completed as challenge_completed_points %}
    """
    bits = token.contents.split()
    if len(bits) < 2:
        raise template.TemplateSyntaxError, "get_points should be formatted 'get_points action [as var]'"
    action = bits[1]
    if len(bits) > 3:
        var = bits[3]
    else:
        var = None
    return GetPointsNode(action, var)
