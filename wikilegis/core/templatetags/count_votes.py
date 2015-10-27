from django.template import Library

register = Library()

@register.filter
def up_votes_count(data):
    return data.filter(vote='up').count()

@register.filter
def down_votes_count(data):
    return data.filter(vote='down').count()

@register.filter
def up_vote(data):
    return data.filter(vote='up').values_list('user_id', flat=True)

@register.filter
def down_vote(data):
    return data.filter(vote='down').values_list('user_id', flat=True)