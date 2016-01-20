# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.models.functions import Lower
from django.http import Http404
from django.shortcuts import redirect, render, get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.utils.text import capfirst
from django.utils.translation import ugettext, ugettext_lazy as _
from django.views.generic import DetailView, CreateView
from .forms import CitizenAmendmentCreationForm, AddProposalForm
from .models import Bill, BillSegment, UpDownVote
from wikilegis.comments2.utils import create_comment
from wikilegis.core.genericdata import BillVideo, BillAuthorData
from wikilegis.core.orderers import SimpleOrderer


class BillOrderer(SimpleOrderer):
    title = _('Order by')
    default = 'date'
    parameter_name = 'order'

    def lookups(self, request):
        return (
            ('date', ugettext('Date')),
            ('title', ugettext('Title')),
        )

    def queryset(self, request, queryset):
        value = self.value()

        if value == 'date':
            queryset = queryset.order_by('-modified')
        elif value == 'title':
            queryset = queryset.order_by(Lower('title').asc())

        return queryset


def index(request):
    if request.GET.get('status') == 'closed':
        bills = Bill.objects.filter(status='closed')
    else:
        bills = Bill.objects.filter(status='published')

    orderer = BillOrderer(request, dict(request.GET.items()))
    bills = orderer.queryset(request, bills)

    return render(request, 'index.html', context=dict(
        bills=bills,
        orderer=orderer,
    ))


def show_bill(request, bill_id):
    bill = get_object_or_404(Bill, pk=bill_id)
    original_segments = bill.segments.filter(original=True)
    new_proposals = bill.segments.filter(original=False, replaced__isnull=True)
    metadata = bill.metadata.all()

    authors = filter(lambda x: x.type == 'AUTHOR', metadata)
    authors = map(BillAuthorData, authors)

    videos = filter(lambda x: x.type == 'VIDEO', metadata)
    videos = map(BillVideo, videos)

    form = AddProposalForm(bill_id=bill_id)

    return render(request, 'bill/bill.html', context=dict(
        bill=bill,
        form=form,
        original_segments=original_segments,
        new_proposals=new_proposals,
        videos=videos,
        authors=authors
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

    return render(request, 'bill/bill_segment.html', context=dict(
        author=author,
        segment=segment,
    ))


def show_proposal(request, bill_id, segment_id):
    segment = _get_segment_or_404(bill_id, segment_id)

    author = segment.bill.metadata.filter(type='AUTHOR').first()
    if author:
        author = BillAuthorData(author)

    if not segment.is_editable():
        return redirect_to_segment_at_bill_page(segment)

    return render(request, 'bill/proposal.html', context=dict(
        author=author,
        segment=segment,
    ))


def show_amendment(request, amendment_id):
    amendment = get_object_or_404(BillSegment, pk=amendment_id)
    url = reverse('show_segment', args=(amendment.bill_id, amendment.replaced_id))
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
            amendment.bill = segment.bill
            amendment.order = 0
            amendment.type = segment.type
            amendment.number = segment.number
            amendment.parent = segment.parent
            amendment.replaced = segment
            amendment.author = request.user
            amendment.original = False

            # TODO what if the content is empty? or exactly like the original? i suggest flash + ignore

            amendment.save()

            comment = form.cleaned_data.get('comment')
            if comment:
                comment = create_comment(request, amendment, request.user, comment)

            messages.success(request, ugettext("{object_type} submitted.").format(
                object_type=capfirst(BillSegment._meta.verbose_name)))

            return redirect(amendment.get_absolute_url())
    else:
        form = form_factory(initial=form_initial_data)

    return render(request, 'bill/create_amendment.html', context=dict(
        form=form,
        segment=segment,
    ))


class CreateProposal(CreateView):
    model = BillSegment
    form_class = AddProposalForm
    template_name = 'bill/create_proposal.html'

    @method_decorator(login_required(login_url='/'))
    def dispatch(self, *args, **kwargs):
        return super(CreateProposal, self).dispatch(*args, **kwargs)

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(CreateProposal, self).get_form_kwargs(**kwargs)
        form_kwargs["bill_id"] = self.kwargs['bill_id']
        return form_kwargs

    def form_valid(self, form):
        import ipdb;ipdb.set_trace()
        amendment = BillSegment()
        amendment.bill_id = self.kwargs['bill_id']
        amendment.type = form.cleaned_data['type']
        amendment.parent = form.cleaned_data['parent']
        amendment.author = self.request.user
        amendment.original = False
        amendment.content = form.cleaned_data['content']
        amendment.save()

        comment = form.cleaned_data.get('comment')
        if comment:
            comment = create_comment(self.request, amendment, self.request.user, comment)

        messages.success(self.request, ugettext("{object_type} submitted.").format(
            object_type=capfirst(BillSegment._meta.verbose_name)))

        return redirect('show_bill', self.kwargs['bill_id'])

    def form_invalid(self, form):
        return redirect('show_bill', self.kwargs['bill_id'])


class BillReport(DetailView):
    model = Bill
    template_name = 'bill/bill_report.html'


def get_votable_object_or_404(user, content_type, object_id):
    content_type = get_object_or_404(ContentType, pk=content_type)
    try:
        content_object = content_type.get_object_for_this_type(pk=object_id)
    except ObjectDoesNotExist:
        raise Http404()
    return content_type, content_object


@login_required
def upvote(request, content_type, object_id):
    return _handle_votes(request, content_type, object_id, True)


@login_required
def downvote(request, content_type, object_id):
    return _handle_votes(request, content_type, object_id, False)


def _handle_votes(request, ctype, object_id, new_vote):
    ctype, obj = get_votable_object_or_404(request.user, ctype, object_id)

    vote, created = UpDownVote.objects\
        .get_or_create(defaults=dict(user_id=request.user.pk, vote=new_vote),
                       user__pk=request.user.pk,
                       object_id=obj.pk,
                       content_type=ctype)
    if not created:
        if vote.vote == new_vote:
            vote.delete()
        else:
            vote.vote = new_vote
            vote.save()

    if not request.is_ajax():
        # TODO FIXME This won't always work. Make sure all votable objects have `get_absolute_url`.
        return redirect(obj.get_absolute_url())
    else:
        return render_to_response('_vote_buttons.html', {
            'content_object': obj,
        }, context_instance=RequestContext(request))
