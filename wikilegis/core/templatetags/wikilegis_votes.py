from core import models
from django.template import Library
from django.contrib.contenttypes.models import ContentType


register = Library()


@register.assignment_tag(takes_context=True)
def voted_by_user(context, instance, vote):
    user = context['request'].user
    if user.is_authenticated():
        try:
            ctype = ContentType.objects.get_for_model(instance)
            updown_vote = models.UpDownVote.objects.get(
                content_type=ctype,
                object_id=instance.id,
                user=user
            )
            if updown_vote.vote == vote:
                return 'voted'
            else:
                return ''
        except models.UpDownVote.DoesNotExist:
            return ''
    else:
        return ''


@register.assignment_tag(takes_context=True)
def order_by_score(context, queryset):
    list_score_id = []
    for proposal in queryset:
        ctype = ContentType.objects.get_for_model(proposal)
        down_vote = models.UpDownVote.objects.filter(content_type=ctype,
                                                     object_id=proposal.id,
                                                     vote=False).count()
        up_vote = models.UpDownVote.objects.filter(content_type=ctype,
                                                   object_id=proposal.id,
                                                   vote=True).count()
        score = up_vote - down_vote
        list_score_id.append((proposal.id, score))
    list_score_id = sorted(list_score_id, key=lambda x: x[1], reverse=True)
    ids = [int(i[0]) for i in list_score_id]
    proposals = list(queryset)
    proposals.sort(key=lambda obj: ids.index(obj.pk))
    return proposals
