import json

from django import template


register = template.Library()


@register.filter()
def json_dumps(obj):
    return json.dumps(obj)


@register.filter()
def split_couple(l):
    return zip(l[0::2], l[1::2])