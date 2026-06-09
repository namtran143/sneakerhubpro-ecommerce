from django import template

register = template.Library()

@register.filter
def star_class(avg, index):
    try:
        avg = float(avg)
        index = int(index)
    except (TypeError, ValueError):
        return 'bi-star'
    return 'bi-star-fill' if avg >= index else 'bi-star'

@register.filter
def multiply(value, arg):
    try:
        return value * arg
    except TypeError:
        return 0
