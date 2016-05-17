# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django import template

register = template.Library()


def get_backend_info(backend):
    backend_info = getattr(settings, 'SOCIAL_BACKEND_INFO', dict())
    assert isinstance(backend_info, dict)
    return backend_info.get(backend)


@register.filter
def social_icon(backend):
    return get_backend_info(backend).get('icon')


@register.filter
def social_title(backend):
    return get_backend_info(backend).get('title')
