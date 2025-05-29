# rf_dispatch/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter(name='attr')
def attr(obj, attr_name):
    """Django template filter to get an attribute of an object dynamically."""
    return getattr(obj, attr_name, '')
