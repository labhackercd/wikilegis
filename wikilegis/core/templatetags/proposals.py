# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from django.contrib.contenttypes.models import ContentType
from django.template import Library
from django_comments.models import Comment
from wikilegis.core.models import BillSegment, UpDownVote

register = Library()


@register.filter
def proposals_count(bill):
    total_proposals = 0
    for segment in bill.segments.filter(original=True):
        total_proposals += segment.substitutes.all().count()
    return total_proposals


@register.filter
def comments_count(bill):
    total_comments = 0
    for segment in bill.segments.all():
        total_comments += segment.comments.count()
    return total_comments


@register.filter
def votes_count(bill):
    total_votes = 0
    for segment in bill.segments.all():
        total_votes += segment.votes.count()
    return total_votes


@register.filter
def contribution_count(bill):
    total_comments = 0
    total_votes = 0
    for segment in bill.segments.all():
        total_comments += segment.comments.count()
        total_votes += segment.votes.count()
    total_proposals = proposals_count(bill)
    return total_comments + total_votes + total_proposals


@register.filter
def attendees_count(bill):
    attendees = []
    segment_ctype = ContentType.objects.get_for_model(BillSegment)
    for segment in bill.segments.all():
        # vote_sgt refers to vote segment
        for vote_sgt in UpDownVote.objects.filter(content_type=segment_ctype, object_id=segment.id):
            attendees.append(vote_sgt.user.id)
        for comment in Comment.objects.filter(object_pk=segment.pk, content_type=segment_ctype):
            attendees.append(comment.user.id)
    total_attendees = len(list(set(attendees)))
    return total_attendees
