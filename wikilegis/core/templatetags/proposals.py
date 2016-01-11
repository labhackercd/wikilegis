# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from django.contrib.contenttypes.models import ContentType
from django.template import Library
from django_comments.models import Comment
from wikilegis.core.models import BillSegment, CitizenAmendment, UpDownVote

register = Library()

@register.filter
def proposals_count(bill):
    total_proposals = 0
    for segment in bill.segments.filter(original=True):
        total_proposals += segment.substitutes.all().count()
    return total_proposals

@register.filter
def attendees_count(bill):
    attendees = []
    segment_ctype = ContentType.objects.get_for_model(BillSegment)
    amendment_ctype = ContentType.objects.get_for_model(CitizenAmendment)
    for segment in bill.segments.all():
        for vote_segment in UpDownVote.objects.filter(content_type=segment_ctype, object_id=segment.id):
            attendees.append(vote_segment.user.id)
        for comment in Comment.objects.filter(object_pk=segment.pk, content_type=segment_ctype):
            attendees.append(comment.user.id)
        for amendment in segment.amendments.all():
            attendees.append(amendment.author.id)
            for vote_amendment in UpDownVote.objects.filter(content_type=amendment_ctype, object_id=amendment.id):
                attendees.append(vote_amendment.user.id)
            for comment in Comment.objects.filter(object_pk=amendment.pk, content_type=amendment_ctype):
                attendees.append(comment.user.id)
    total_attendees = len(list(set(attendees)))
    return total_attendees