from django.forms import widgets
from . import nocontext

@nocontext
def render_field(field, *args, **kwargs):
    extra_classes = kwargs.pop('extra_classes', [])

    widget = kwargs.pop('widget', None)
    if widget is not None:
        if isinstance(widget, basestring):
            widget_name = widget
            widget = getattr(widgets, widget_name, None)
            assert widget, NameError("Undefined widget: '{0}'".format(widget_name))
            widget = widget()

    attrs = {
        'class': extra_classes,
    }

    return field.as_widget(widget=widget, attrs=attrs)
