import simplejson
from datetime import datetime

def to_json(obj):
    if isinstance(obj, datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    return obj

def model_to_dict(model):
    c = {}
    table = model.__table__
    for key in table.c.keys():
        c[key] = to_json(getattr(model, key))
    return c

def model_to_yaml(model):
    from yaml import load, dump
    return dump(model_to_dict(model))

def model_to_json(model):
    """
    """
    return simplejson.dumps(model_to_dict(model))
