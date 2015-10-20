# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.text import capfirst
from django.utils.translation import ugettext
from django.views.generic import DetailView

from .forms import CitizenAmendmentCreationForm
from .models import Bill, BillSegment, CitizenAmendment, UserSegmentChoice, GenericData
from wikilegis.comments2.utils import create_comment
from wikilegis.core.genericdata import BillVideo, BillAuthorData


def index(request):
    bills = Bill.objects.exclude(status='1')

    return render(request, 'index.html', context=dict(
        bills=bills,
    ))


def show_bill(request, bill_id):
    bill = get_object_or_404(Bill, pk=bill_id)

    metadata = bill.metadata.all()

    authors = filter(lambda x: x.type == 'AUTHOR', metadata)
    authors = map(BillAuthorData, authors)

    videos = filter(lambda x: x.type == 'VIDEO', metadata)
    videos = map(BillVideo, videos)

    # XXX Lambda to make it lazy :D
    total_amendment_count = lambda: CitizenAmendment.objects.filter(segment__bill__id=bill.id).count()

    return render(request, 'bill/bill.html', context=dict(
        bill=bill,
        videos=videos,
        authors=authors,
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

    author = segment.bill.metadata.filter(type='AUTHOR').first()
    if author:
        author = BillAuthorData(author)

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

    return render(request, 'bill/bill_segment.html', context=dict(
        author=author,
        segment=segment,
        chosen_amendment=chosen_amendment,
        chosen_amendment_id=chosen_amendment_id,
    ))


def show_amendment(request, amendment_id):
    amendment = get_object_or_404(CitizenAmendment, pk=amendment_id)
    url = reverse('show_segment', args=(amendment.segment.bill_id, amendment.segment_id))
    url += '#' + amendment.html_id()
    return redirect(url)


@login_required
def create_amendment(request, bill_id, segment_id):
    segment = _get_segment_or_404(bill_id, segment_id)

    if not segment.is_editable():
        messages.error(request, ugettext(
            "Cannot submit proposals to {object}.").format(object=segment))
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

            comment = form.cleaned_data.get('comment')
            if comment:
                comment = create_comment(request, amendment, request.user, comment)

            messages.success(request, ugettext("{object_type} submitted.").format(
                object_type=capfirst(CitizenAmendment._meta.verbose_name)))

            return redirect(amendment.get_absolute_url())
    else:
        form = form_factory(initial=form_initial_data)

    return render(request, 'bill/create_amendment.html', context=dict(
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

    redirect_url = None
    if amendment is not None:
        redirect_url = amendment.get_absolute_url()
    else:
        redirect_url = reverse('show_segment', args=[bill_id, segment_id])

    return redirect(redirect_url)


@login_required
def unchoose_amendment(request, bill_id, segment_id):
    UserSegmentChoice.objects\
        .filter(user=request.user, segment__id=segment_id, segment__bill__id=bill_id)\
        .delete()

    return redirect('show_segment', bill_id=bill_id, segment_id=segment_id)


class BillReport(DetailView):
    model = Bill
    template_name = 'bill/bill_report.html'

