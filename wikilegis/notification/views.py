from django.http import JsonResponse
from django.template.loader import render_to_string

from notification.models import Newsletter


def render_newsletter_info(request, bill_id=None):
    newsletter, created = Newsletter.objects.get_or_create(user=request.user,
                                                           bill_id=bill_id)
    if created:
        newsletter.periodicity = request.POST.get('periodicity')
        newsletter.save()
    else:
        if newsletter.is_active:
            newsletter.is_active = False
        else:
            newsletter.is_active = True
            newsletter.periodicity = request.POST.get('periodicity')
        newsletter.save()

    html = render_to_string('bill/_newsletter.html', {'request': request,
                                                      'bill_id': bill_id})
    return JsonResponse({'html': html})
