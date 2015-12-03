# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import
from django.template import Library

register = Library()

@register.simple_tag
def proposals_count(bill):
    total_proposals = 0
    for segment in bill.segments.all():
        total_proposals += segment.amendments.all().count()
    return total_proposals