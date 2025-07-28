from django import template

register = template.Library()

@register.filter
def dont_return_none(value):
    if value:
        return value
    
    return ''