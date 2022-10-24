"""Source: https://github.com/HackSoftware/Django-Styleguide-Example/blob/master/styleguide_example/common/utils.py"""
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.core.exceptions import ImproperlyConfigured

from rest_framework import serializers


def create_serializer_class(name, fields):
    """
    Source: https://github.com/HackSoftware/Django-Styleguide-Example/blob/master/styleguide_example/common/utils.py
    """
    return type(name, (serializers.Serializer,), fields)


def inline_serializer(*, fields, data=None, **kwargs):
    """
    Source: https://github.com/HackSoftware/Django-Styleguide-Example/blob/master/styleguide_example/common/utils.py
    """
    serializer_class = create_serializer_class(name='', fields=fields)

    if data is not None:
        return serializer_class(data=data, **kwargs)

    return serializer_class(**kwargs)
