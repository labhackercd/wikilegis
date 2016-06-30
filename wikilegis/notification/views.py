from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from wikilegis.notification.models import Newsletter


def verify_newsletter(request, bill_id=None):
    newsletter, created = Newsletter.objects.get_or_create(user=request.user, bill_id=bill_id)
    if created:
        newsletter.periodicity = request.GET.get('periodicity')
        newsletter.save()
    else:
        if newsletter.status:
            newsletter.status = False
        else:
            newsletter.status = True
            newsletter.periodicity = request.GET.get('periodicity')
        newsletter.save()

    return HttpResponseRedirect(reverse('show_bill', kwargs={'pk': bill_id}))
