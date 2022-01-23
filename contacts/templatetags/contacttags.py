from django import template
register = template.Library()

@register.filter(name="decode_col", is_safe=True)
def decode_col(iterable, num):
    return getattr(iterable, num)