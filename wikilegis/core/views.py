from django.shortcuts import render, get_object_or_404
from .models import Bill, CitizenAmendment

def index(request):
    bills = Bill.objects.all()

    return render(request, 'index.html', context=dict(
        bills=bills
    ))


def show_bill(request, bill_id):
    bill = get_object_or_404(Bill, pk=bill_id)

    amendments = CitizenAmendment.objects.filter(segment__bill=bill)

    return render(request, 'bill.html', context=dict(
        bill=bill,
        amendments=amendments
    ))
