# -*- coding: utf-8 -*-
from django.template import Library

from wikilegis.core.models import BillSegment

register = Library()


@register.filter
def previous(segment):
    try:
        article = BillSegment.objects.filter(bill_id=segment.bill_id, original=True,
                                             order__lt=segment.order, type__name='Artigo').order_by('-order')[0]
        previous_segment = BillSegment.objects.filter(bill_id=segment.bill_id, original=True,
                                                      order__lt=segment.order, order__gte=article.order)
        return previous_segment
    except:
        return {}


@register.filter
def previous_article(segment):
    # import ipdb; ipdb.set_trace()
    try:
        if segment.type.name != "Artigo":
            article = BillSegment.objects.filter(bill_id=segment.bill_id, original=True,
                                                 order__lt=segment.order, type__name='Artigo').order_by('-order')[0]
            return article
    except:
        return {}
