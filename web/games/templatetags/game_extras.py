from django import template
from web.instances.models import PointsAssignment

register = template.Library()

class GlobalPointsNode(template.Node):
    def __init__(self, action, category):
        self.category = template.Variable(category)
        self.action = action

    def render(self, context):
        instance = context['instance']
    
        try:
            self.category = self.category.resolve(context)
            self.category = self.category.game_type
            self.action = str(self.action)

            if self.action == "all":
                values = PointsAssignment.objects.filter(instance=instance, action__icontains=self.category).values('points')
            else:
                test= "%s_%s" % (self.category, self.action)
                values = PointsAssignment.objects.filter(instance=instance, action="%s_%s" % (self.category, self.action)).values('points')

            values = [thing['points'] for thing in values]
        except template.VariableDoesNotExist:
            if self.action == "all":
                values = PointsAssignment.objects.filter(instance=instance, action__icontains=self.category).values('points')
            else:
                values = PointsAssignment.objects.filter(instance=instance, action="%s_%s" % (self.category, self.action)).values('points')

            values = [thing['points'] for thing in values]
        except AttributeError:
            return 0
        
        return sum(values)
    

@register.tag(name="get_points")
def do_get_points(parser, token):
    """
      usage: {% get_points for completed action_type %}
      usage: {% get_points for created action_type %}
      usage: {% get_points for all action_type %}
    """
    bits = token.contents.split()
    if len(bits) != 4:
        raise TemplateSyntaxError, "get_points should be formatted 'get_points for all/[action] category"
    elif bits[1] != 'for':
        raise TemplateSyntaxError, "'for' should be the second word"
    return GlobalPointsNode(bits[2], bits[3])
