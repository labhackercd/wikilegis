from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render, get_object_or_404

from .forms import CitizenAmendmentCreationForm
from .models import Bill, BillSegment, CitizenAmendment, UserSegmentChoice


def index(request):
    bills = Bill.objects.all()

    return render(request, 'index.html', context=dict(
        bills=bills,
    ))


def show_bill(request, bill_id):
    bill = get_object_or_404(Bill, pk=bill_id)

    # XXX Lambda to make it lazy :D
    total_amendment_count = lambda: CitizenAmendment.objects.filter(segment__bill__id=bill.id).count()

    return render(request, 'bill.html', context=dict(
        bill=bill,
        total_amendment_count=total_amendment_count,
    ))


def _get_segment_or_404(bill_id, segment_id):
    return get_object_or_404(BillSegment, pk=segment_id, bill__id=bill_id)


def redirect_to_segment_at_bill_page(segment):
    return redirect_to_segment_at_bill_page_2(segment.bill.id, segment.id)


def redirect_to_segment_at_bill_page_2(bill_id, segment_id):
    segment_url = reverse('show_bill', kwargs=dict(bill_id=bill_id))

    # Anchor right into the requested segment.
    segment_url += '#segment-{0}'.format(segment_id)

    return redirect(segment_url)



def show_segment(request, bill_id, segment_id):
    segment = _get_segment_or_404(bill_id, segment_id)

    if not segment.is_editable():
        return redirect_to_segment_at_bill_page(segment)

    chosen_amendment = None
    chosen_amendment_id = None
    if request.user.is_authenticated():
        chosen_amendment = UserSegmentChoice.objects \
            .filter(user=request.user, segment__id=segment_id, segment__bill__id=bill_id) \
            .first()
        if chosen_amendment is not None:
            chosen_amendment_id = chosen_amendment.amendment.id if chosen_amendment.amendment is not None else 'original'

    return render(request, 'segment.html', context=dict(
        segment=segment,
        chosen_amendment=chosen_amendment,
        chosen_amendment_id=chosen_amendment_id,
    ))


@login_required
def create_amendment(request, bill_id, segment_id):
    segment = _get_segment_or_404(bill_id, segment_id)

    if not segment.is_editable():
        # TODO flash message?
        return redirect_to_segment_at_bill_page(segment)

    form_factory = CitizenAmendmentCreationForm
    form_initial_data = {
        'content': segment.content,
    }

    if request.method == 'POST':
        form = form_factory(request.POST, initial=form_initial_data)

        if form.is_valid():
            amendment = form.save(commit=False)
            amendment.author = request.user
            amendment.segment = segment

            # TODO what if the content is empty? or exactly like the original? i suggest flash + ignore

            amendment.save()

            # TODO flash message?

            redirect_url = reverse('show_segment', kwargs=dict(bill_id=bill_id, segment_id=segment_id))

            return redirect(redirect_url)
    else:
        form = form_factory(initial=form_initial_data)

    return render(request, 'create_amendment.html', context=dict(
        form=form,
        segment=segment,
    ))


@login_required
def choose_amendment(request, bill_id, segment_id, amendment_id):

    if amendment_id == 'original':
        amendment = None
    else:
        amendment = get_object_or_404(CitizenAmendment, id=amendment_id,
                                      segment__id=segment_id, segment__bill__id=bill_id)

    choice = UserSegmentChoice.objects.filter(user=request.user, segment__id=segment_id, segment__bill__id=bill_id).first()
    if choice is None:
        choice = UserSegmentChoice.objects.create(user=request.user, segment_id=segment_id, amendment=amendment)
    else:
        choice.amendment = amendment
        choice.save()

    return redirect('show_segment', bill_id=bill_id, segment_id=segment_id)


@login_required
def unchoose_amendment(request, bill_id, segment_id):
    UserSegmentChoice.objects\
        .filter(user=request.user, segment__id=segment_id, segment__bill__id=bill_id)\
        .delete()

    return redirect('show_segment', bill_id=bill_id, segment_id=segment_id)
