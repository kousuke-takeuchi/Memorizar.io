import json

from django import template


register = template.Library()


@register.filter()
def json_dumps(obj):
    return json.dumps(obj)