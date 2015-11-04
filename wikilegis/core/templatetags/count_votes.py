from django.contrib.contenttypes.models import ContentType
from django.template import Library
from wikilegis.core.models import UpDownVote, BillSegment, CitizenAmendment

register = Library()

@register.filter
def segment_up_votes_count(data):
    return UpDownVote.objects.filter(object_id=data, vote=1,
                                     content_type=ContentType.objects.get_for_model(BillSegment)).count()

@register.filter
def segment_down_votes_count(data):
    return UpDownVote.objects.filter(object_id=data, vote=0,
                                     content_type=ContentType.objects.get_for_model(BillSegment)).count()

@register.filter
def amendment_up_votes_count(data):
    return UpDownVote.objects.filter(object_id=data, vote=1,
                                     content_type=ContentType.objects.get_for_model(CitizenAmendment)).count()

@register.filter
def amendment_down_votes_count(data):
    return UpDownVote.objects.filter(object_id=data, vote=0,
                                     content_type=ContentType.objects.get_for_model(CitizenAmendment)).count()


@register.filter
def segment_up_vote(data):
    return UpDownVote.objects.filter(object_id=data, vote=1,
                                     content_type=ContentType.objects.get_for_model(BillSegment)).values_list('user_id',
                                                                                                              flat=True)

@register.filter
def segment_down_vote(data):
    return UpDownVote.objects.filter(object_id=data, vote=0,
                                     content_type=ContentType.objects.get_for_model(BillSegment)).values_list('user_id',
                                                                                                              flat=True)


@register.filter
def amendment_up_vote(data):
    return UpDownVote.objects.filter(object_id=data, vote=1,
                                     content_type=ContentType.objects.get_for_model(CitizenAmendment)
                                     ).values_list('user_id', flat=True)

@register.filter
def amendment_down_vote(data):
    return UpDownVote.objects.filter(object_id=data, vote=0,
                                     content_type=ContentType.objects.get_for_model(CitizenAmendment)
                                     ).values_list('user_id', flat=True)
