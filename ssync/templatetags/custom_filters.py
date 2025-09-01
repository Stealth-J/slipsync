from django import template
from types import SimpleNamespace
import json
from datetime import datetime

register = template.Library()

@register.filter
def dont_return_none(value):
    if value:
        return value
    
    return ''


@register.filter
def convert_to_json(objs_):
    objs_ = [ json.dumps(vars(obj_)) for obj_ in objs_ if isinstance(obj_, SimpleNamespace) ]
    final_string = '||'.join(objs_)

    print(type(final_string), final_string)
    return final_string


@register.filter
def current_time(something):
    return datetime.now()