# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import force_text
from wikilegis.helpers import nocontext
from wikilegis.helpers import helpers
from wikilegis.helpers.utils import parse_extra_classes


@nocontext
def render_field(field, *args, **kwargs):
    extra_classes = kwargs.pop('extra_classes', [])
    extra_classes = parse_extra_classes(extra_classes)

    if field.errors:
        extra_classes.append('invalid')

    kwargs['extra_classes'] = extra_classes

    field_errors = force_text(field.errors) if field.errors else ''

    return '\n'.join([
        helpers.render_field(None, field, *args, **kwargs),
        field.label_tag(),
        field_errors,
    ])
