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


@register.filter
def sort_by_keys(value, keys):
    transformed = []
    for key in keys.split(','):
        factor = 1
        if key.startswith('-'):
            key = key.replace('-', '')
            factor = -1
        transformed.append((key, factor))

    def compare(item1, item2):
        for (key, factor) in transformed:
            result = factor * cmp(getattr(item1, key), getattr(item2, key))
            if result != 0:
                return result
        return 0

    return sorted(list(value), cmp=compare)

sort_by_key = register.filter('sort_by_key', sort_by_keys)
