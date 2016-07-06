# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from operator import itemgetter
from django.contrib.contenttypes.models import ContentType
from django.template import Library
from wikilegis.core.models import UpDownVote

from templatetag_sugar.register import tag
from templatetag_sugar.parser import Name, Variable, Constant, Optional


register = Library()


@register.filter
def content_type(obj):
    if not obj:
        return None
    return ContentType.objects.get_for_model(obj)


@register.simple_tag
def get_upvote_count(content_object):
    ctype = ContentType.objects.get_for_model(content_object)
    return UpDownVote.objects.filter(content_type=ctype, object_id=content_object.id, vote=True).count()


@register.simple_tag
def get_downvote_count(content_object):
    ctype = ContentType.objects.get_for_model(content_object)
    return UpDownVote.objects.filter(content_type=ctype, object_id=content_object.id, vote=False).count()


@register.simple_tag
def get_vote_score(content_object):
    ctype = ContentType.objects.get_for_model(content_object)
    down_vote = UpDownVote.objects.filter(content_type=ctype,
                                          object_id=content_object.id, vote=False).count()
    up_vote = UpDownVote.objects.filter(content_type=ctype,
                                        object_id=content_object.id, vote=True).count()
    return up_vote - down_vote


@tag(register, [Constant("for"), Variable(), Optional([Constant("as"), Name()])])
def order_by_score(context, queryset, name=None):
    list_score_id = []
    for proposal in queryset:
        ctype = ContentType.objects.get_for_model(proposal)
        down_vote = UpDownVote.objects.filter(content_type=ctype,
                                              object_id=proposal.id, vote=False).count()
        up_vote = UpDownVote.objects.filter(content_type=ctype,
                                            object_id=proposal.id, vote=True).count()
        score = up_vote - down_vote
        list_score_id.append((proposal.id, score))
    list_score_id = sorted(list_score_id, key=lambda x: x[1], reverse=True)
    ids = [int(i[0]) for i in list_score_id]
    proposals = list(queryset)
    proposals.sort(key=lambda obj: ids.index(obj.pk))
    if name is not None:
        context[name] = proposals
        return ''
    else:
        return proposals


@tag(register, [Variable(), Variable(), Optional([Constant("as"), Name()])])
def get_user_vote_for(context, user, content_object, name=None):
    if not user.is_anonymous():
        try:
            ctype = ContentType.objects.get_for_model(content_object)
            vote = UpDownVote.objects.get(user__pk=user.pk, content_type=ctype, object_id=content_object.id).vote
        except UpDownVote.DoesNotExist:
            vote = None
    else:
        vote = None

    if name is not None:
        context[name] = vote
        return ''
    else:
        return vote
