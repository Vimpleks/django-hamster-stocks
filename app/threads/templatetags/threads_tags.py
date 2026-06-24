from django import template
from decimal import Decimal


register = template.Library()


@register.filter
def remove_trailing_zeros(value):
    """
    Убирает нули после запятой без округления.
    """
    if value is None:
        return ''
    value = Decimal(str(value))
    return str(value.normalize())
