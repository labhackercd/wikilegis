from django.template import Library

register = Library()


@register.filter
def amendments_count(amendments, amendment_type):
    results = [a for a in amendments if a.__class__.__name__ == amendment_type]
    return len(results)
