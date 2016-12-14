from functools import wraps
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseForbidden
from wikilegis.core.models import BillSegment


def open_for_partifipations(view_method):
    def _open_for_participations(request, *args, **kwargs):
        segment = BillSegment.objects.get(pk=kwargs.get('segment_id'))
        if segment.bill.status not in ['published', 'unlisted']:
            msg = _("Bill closed for participations.")
            return HttpResponseForbidden(reason=msg)
        response = view_method(request, *args, **kwargs)
        return response
    return wraps(view_method)(_open_for_participations)
