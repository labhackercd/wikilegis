# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.template import Library
from django.template.loader import render_to_string

register = Library()


@register.simple_tag(takes_context=True)
def render_comments(context, content_object):
    context_dict = {}
    for d in context.dicts:
        context_dict.update(d)

    context_dict['content_object'] = content_object

    if hasattr(content_object, 'get_absolute_url'):
        context_dict['next'] = content_object.get_absolute_url()

    return render_to_string('comments2/_render_comments.html', context_dict)
