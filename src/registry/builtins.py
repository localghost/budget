from django import template
from collections import OrderedDict

register = template.Library()

@register.filter(name='sort')
def filter_sort(value):
    if isinstance(value, dict):
        return OrderedDict(value, key=lambda item: item[0].lower)
    elif isinstance(value, (list, tuple)):
        return sorted(value)
    return value

@register.filter(name='sign')
def filter_sign(value):
    return '%+.2f' % value
    