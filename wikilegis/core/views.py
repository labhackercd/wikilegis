# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.http import Http404
from django.shortcuts import redirect, render, get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.utils.text import capfirst
from django.utils.translation import ugettext, ugettext_lazy as _
from django.views.generic import DetailView, CreateView
from django.contrib.sites.models import Site

from .forms import CitizenAmendmentCreationForm, AddProposalForm
from .models import Bill, BillSegment, UpDownVote, Proposition
from django_comments.models import Comment
from django.conf import settings
from wikilegis.auth2.models import Congressman
from wikilegis.comments2.utils import create_comment
from wikilegis.core.genericdata import BillVideo, BillAuthorData
from wikilegis.core.orderers import SimpleOrderer


class BillOrderer(SimpleOrderer):
    title = _('Order by')
    default = 'hot'
    parameter_name = 'order'

    def lookups(self, request):
        return (
            ('hot', ugettext('Hot')),
            ('date', ugettext('Date')),
        )

    def queryset(self, request, queryset):
        value = self.value()
        queryset = queryset.annotate(
            score=Count('segments__substitutes')
        )
        if value == 'date':
            queryset = queryset.order_by('-modified')
        elif value == 'hot':
            queryset = queryset.order_by('-score')

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


class BillDetailView(DetailView):
    model = Bill
    template_name = 'bill/bill.html'

    def get_context_data(self, **kwargs):
        context = super(BillDetailView, self).get_context_data(**kwargs)
        metadata = self.object.metadata.all()
        videos = filter(lambda x: x.type == 'VIDEO', metadata)
        segment_ctype = ContentType.objects.get_for_model(BillSegment)
        segments_id = set(self.object.segments.values_list('id', flat=True))
        votes_ids = UpDownVote.objects.filter(content_type=segment_ctype,
                                              object_id__in=segments_id).values_list('user__id', flat=True)
        comment_ids = Comment.objects.filter(object_pk__in=segments_id,
                                             content_type=segment_ctype).values_list('user__id', flat=True)
        proposals_ids = self.object.segments.filter(original=False).values_list('author__id', flat=True)
        context['attendees'] = len(set(list(votes_ids) + list(comment_ids) + list(proposals_ids)))
        context['proposals'] = self.object.segments.filter(original=False).count()
        context['videos'] = map(BillVideo, videos)
        context['domain'] = Site.objects.get_current().domain + settings.FORCE_SCRIPT_NAME
        try:
            context['congressman'] = Congressman.objects.filter(user_id=self.object.reporting_member.id).latest('id')
        except:
            pass
        try:
            context['proposition'] = Proposition.objects.filter(bill_id=self.object.id).values(
                'id', 'situation', 'id_proposition', 'id_register', 'author', 'party_author', 'uf_author').latest('id')
        except:
            pass
        context['original_segments'] = self.object.segments.filter(original=True).annotate(
            proposals_count=Count('substitutes'))
        return context


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

    def get_context_data(self, **kwargs):
        context = super(BillReport, self).get_context_data(**kwargs)
        segment_ctype = ContentType.objects.get_for_model(BillSegment)
        segments_id = set(self.object.segments.values_list('id', flat=True))
        votes = UpDownVote.objects.filter(content_type=segment_ctype, object_id__in=segments_id)
        comments = Comment.objects.filter(object_pk__in=segments_id, content_type=segment_ctype)
        proposals = self.object.segments.filter(original=False)
        featured_segments = (list(votes.values_list('object_id', flat=True)) +
                             list(comments.values_list('object_pk', flat=True)) +
                             list(proposals.values_list('replaced_id', flat=True)))
        featured_segments = set(map(int, featured_segments))
        context['votes'] = votes.count()
        context['comments'] = comments.count()
        context['attendees'] = len(set(list(votes.values_list('user__id', flat=True)) +
                                       list(comments.values_list('user__id', flat=True)) +
                                       list(proposals.values_list('author__id', flat=True))))
        context['proposals'] = proposals.count()
        context['original_segments'] = self.object.segments.filter(
            original=True, id__in=featured_segments).annotate(proposals_count=Count('substitutes'))
        return context


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
