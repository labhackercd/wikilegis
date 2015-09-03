from django.shortcuts import render, get_object_or_404
from .models import Bill, BillSegment, CitizenAmendment

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

    return render(request, 'segment.html', context=dict(
        segment=segment,
    ))
