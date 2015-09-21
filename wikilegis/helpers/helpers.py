# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.forms import widgets
from . import nocontext, utils


@nocontext
def render_field(field, *args, **kwargs):
    extra_classes = kwargs.pop('extra_classes', [])
    extra_classes = utils.parse_extra_classes(extra_classes)

    widget = kwargs.pop('widget', None)
    if widget is not None:
        if isinstance(widget, basestring):
            widget_name = widget
            widget = getattr(widgets, widget_name, None)
            assert widget, NameError("Undefined widget: '{0}'".format(widget_name))
            widget = widget()

    attrs = {
        'class': ' '.join(extra_classes),
    }

    return field.as_widget(widget=widget, attrs=attrs)
