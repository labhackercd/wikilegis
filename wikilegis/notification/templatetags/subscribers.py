# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from django.template import Library
from wikilegis.notification.models import Newsletter

register = Library()


@register.assignment_tag()
def subscriber(bill_id, user_id):
    try:
        newsletter = Newsletter.objects.get(bill_id=bill_id, user_id=user_id)
        return newsletter.status
    except ObjectDoesNotExist:
        return False
