# encoding: UTF-8

"""
Module for common stuff, such as model to json conversions.
"""

import json
from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder


def model_to_json(model):
    """
    Serialize a model to Json:
    - model: the model object to serialize.
    Return: the json as a string
    """
    dictionnary = model_to_dict(model)
    return json.dumps(dictionnary, cls=DjangoJSONEncoder)


def queryset_to_json(queryset):
    """
    Serialize a queryset to Json:
    - queryset: the queryset to serialize.
    Return: the json as a string
    """
    list_dicts = [model_to_dict(m) for m in list(queryset)]
    return json.dumps(list_dicts, cls=DjangoJSONEncoder)


def json_to_model(text, model_class):
    """
    Deserialize json string into model instances:
    - text: json source as a string
    - model_class: the model class
    Return: a model instance
    """
    fields = json.loads(text)
    return model_class.objects.create(**fields)
