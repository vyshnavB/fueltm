import datetime
from django import template

register = template.Library()

@register.filter
def fromunix(value):
    return datetime.datetime.fromtimestamp(int(value))