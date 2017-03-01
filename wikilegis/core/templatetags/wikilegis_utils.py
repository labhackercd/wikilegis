from core import models
from django.template import Library
from django.utils.module_loading import import_module


register = Library()


@register.assignment_tag(takes_context=True)
def get_segment_types(context):
    segment = context['segment']
    return models.SegmentType.objects.exclude(
        id=segment.segment_type.id
    ).exclude(editable=False)


@register.filter
def is_instance(value, class_str):
    split = class_str.split('.')
    return isinstance(
        value,
        getattr(import_module('.'.join(split[:-1])), split[-1])
    )
