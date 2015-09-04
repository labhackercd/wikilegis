from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render, get_object_or_404
from .models import Bill, BillSegment

def index(request):
    bills = Bill.objects.all()

    return render(request, 'index.html', context=dict(
        bills=bills,
    ))


def show_bill(request, bill_id):
    bill = get_object_or_404(Bill, pk=bill_id)

    return render(request, 'bill.html', context=dict(
        bill=bill,
    ))


def show_segment(request, bill_id, segment_id):
    segment = get_object_or_404(BillSegment, pk=segment_id, bill__id=bill_id)

    if not segment.is_editable():
        segment_url = reverse('show_bill', kwargs=dict(bill_id=segment.bill.id))

        # Anchor right into the requested segment.
        segment_url += '#segment-{0}'.format(segment.id)

        return redirect(segment_url)

    return render(request, 'segment.html', context=dict(
        segment=segment,
    ))
