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
