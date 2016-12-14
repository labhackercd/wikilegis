# -*- coding: utf-8 -*-
from django.template import Library
register = Library()


@register.filter
def amendments_count(segment):
    return segment.substitutes.all().count()
