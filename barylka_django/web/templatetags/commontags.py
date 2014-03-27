from django import template
register = template.Library()

@register.filter
def key(d, key_name):
    return d[key_name]

@register.filter
def toInt(d):
    return int(d)

key = register.filter('key', key)
toInt = register.filter('toInt', toInt)

