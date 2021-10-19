import json

from django import template

from social_django.models import UserSocialAuth


register = template.Library()


@register.filter()
def json_dumps(obj):
    return json.dumps(obj)


@register.filter()
def user_avatar(user):
    social_auth = UserSocialAuth.objects.get(user=user)
    return social_auth.extra_data['picture']



@register.filter()
def split_couple(l):
    return zip(l[0::2], l[1::2])


@register.filter()
def display_timedelta(elapsed_time):
    elapsed_hour = elapsed_time // 3600
    elapsed_minute = (elapsed_time % 3600) // 60
    elapsed_second = (elapsed_time % 3600 % 60)

    if elapsed_hour > 0:
        if elapsed_minute > 0:
            if elapsed_second > 0:
                display_str = str(elapsed_hour) + "時間" + str(elapsed_minute) + "分" + str(elapsed_second) + "秒"
            else:
                display_str = str(elapsed_hour) + "時間" + str(elapsed_minute) + "分"
        else:
            if elapsed_second > 0:
                display_str = str(elapsed_minute) + "分" + str(elapsed_second) + "秒"
            else:
                display_str = str(elapsed_minute) + "分"
    else:
        if elapsed_minute > 0:
            if elapsed_second > 0:
                display_str = str(elapsed_minute) + "分" + str(elapsed_second) + "秒"
            else:
                display_str = str(elapsed_second) + "分"
        else:
            if elapsed_second > 0:
                display_str = str(elapsed_second) + "秒"
            else:
                display_str = str(elapsed_second) + "秒"
    return display_str


@register.simple_tag
def to_json(obj, *fields, **kwargs):
    print(obj)
    many = kwargs.get('many', True)
    to_str = kwargs.get('to_str', '')
    to_str = to_str.split()
    if many:
        data = []
        for o in obj:
            d = {}
            for field in fields:
                value = getattr(o, field)
                if field in to_str:
                    value = str(value)
                d[field] = value
            data.append(d)
    else:
        data = {}
        for field in fields:
            value = getattr(obj, field)
            if field in to_str:
                value = str(value)
            data[field] = value
    return json.dumps(data)