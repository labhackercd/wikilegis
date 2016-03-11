from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from annoying.decorators import ajax_request
from wikilegis.notification.models import Newsletter


@ajax_request
def verify_newsletter(request, bill_id=None, periodicity=None):
    newsletter, created = Newsletter.objects.get_or_create(user=request.user, bill_id=bill_id)
    if created:
        newsletter.periodicity = periodicity
        newsletter.save()
    else:
        if newsletter.status:
            newsletter.status = False
        else:
            newsletter.status = True
            newsletter.periodicity = periodicity
        newsletter.save()

    return HttpResponseRedirect(reverse('show_bill', kwargs={'bill_id': bill_id}))
