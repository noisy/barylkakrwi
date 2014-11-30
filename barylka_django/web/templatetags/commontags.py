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
    _list = list(value)

    def compare(item1, item2):
        for key in item1.__keys_for_sort.split(','):

            if key.startswith('-'):
                key = key.replace('-', '')

                if getattr(item1, key) > getattr(item2, key):
                    return -1
                elif getattr(item1, key) < getattr(item2, key):
                    return 1
            else:
                if getattr(item1, key) < getattr(item2, key):
                    return -1
                elif getattr(item1, key) > getattr(item2, key):
                    return 1

        return 0

    for item in _list:
        setattr(item, '__keys_for_sort', keys)

    _list = sorted(_list, cmp=compare)

    for item in _list:
        delattr(item, '__keys_for_sort')

    return _list


sort_by_key = register.filter('sort_by_key', sort_by_keys)
