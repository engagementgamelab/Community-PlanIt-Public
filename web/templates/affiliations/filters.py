@register.filter(name='split')
@stringfilter
def split(delimiter, arg):
    return value.split(arg)
