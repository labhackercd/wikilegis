from django.http import JsonResponse, Http404
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.views.generic import DetailView
from django.views.decorators.clickjacking import xframe_options_exempt
from distutils.util import strtobool
from django.contrib.sites.models import Site
from django.db.models import Q

from core import models, model_mixins


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['open_private_bills'] = models.Bill.objects.none()
        context['closed_private_bills'] = models.Bill.objects.none()
        if self.request.user.is_authenticated():
            context['open_private_bills'] = self.request.user.allowed_bills.filter(
                status='published', is_visible=True).order_by('-created')
            context['closed_private_bills'] = self.request.user.allowed_bills.filter(
                status='closed', is_visible=True).order_by('-created')
        context['open_bills'] = models.Bill.objects.filter(
            status='published', is_visible=True,
            allowed_users__isnull=True).order_by('-created')
        context['closed_bills'] = models.Bill.objects.filter(
            status='closed', is_visible=True,
            allowed_users__isnull=True).order_by('-created')
        context['prefix_url'] = settings.FORCE_SCRIPT_NAME
        return context


@method_decorator(xframe_options_exempt, name='dispatch')
class WidgetView(DetailView):
    model = models.Bill
    template_name = 'widget.html'

    def get_context_data(self, **kwargs):
        context = super(WidgetView, self).get_context_data(**kwargs)
        context['prefix_url'] = settings.FORCE_SCRIPT_NAME
        return context


def render_404(message):
    return JsonResponse(
        {'title': _('404 Error'),
         'message': message},
        status=404
    )


def render_bill_info(request, bill_id):
    try:
        bill = models.Bill.objects.get(pk=bill_id)
        if bill.status == 'draft':
            raise ObjectDoesNotExist

        if bill.allowed_users.all():
            if request.user not in bill.allowed_users.all():
                raise ObjectDoesNotExist

        html = render_to_string('bill/_info.html', {'request': request,
                                                    'bill': bill})
        return JsonResponse({'html': html})
    except ObjectDoesNotExist:
        message = _('The following URL has returned no known bill: '
                    '<br> <strong>{}/bill/{}</strong>')
        return render_404(_(message.format(request.get_host(), bill_id)))


def render_bill_content(request, bill_id):
    try:
        bill = models.Bill.objects.get(pk=bill_id)
        if bill.status == 'draft':
            raise ObjectDoesNotExist

        if bill.allowed_users.all():
            if request.user not in bill.allowed_users.all():
                raise ObjectDoesNotExist

        html = render_to_string('bill/_content.html', {'request': request,
                                                       'bill': bill})
        return JsonResponse({'html': html})
    except ObjectDoesNotExist:
        message = _('The following URL has returned no known bill: '
                    '<br> <strong>{}/bill/{}</strong>')
        return render_404(_(message.format(request.get_host(), bill_id)))


def render_bill_amendments(request, segment_id):
    try:
        segment = models.BillSegment.objects.get(pk=segment_id)
        if segment.bill.status == 'draft':
            raise ObjectDoesNotExist

        if segment.bill.allowed_users.all():
            if request.user not in segment.bill.allowed_users.all():
                raise ObjectDoesNotExist

        html = render_to_string('amendments/_index.html', {'request': request,
                                                           'segment': segment})
        return JsonResponse({'html': html})
    except ObjectDoesNotExist:
        message = _('The following URL has returned no known segment.')
        path = request.path.replace('render/', '')
        return render_404(_(message.format(request.get_host(), path)))


def render_amendment_segment(request, segment_id):
    segment = get_object_or_404(models.BillSegment, pk=segment_id)
    html = render_to_string('amendments/_segment.html', {'request': request,
                                                         'segment': segment})
    return JsonResponse({'html': html})


def render_amendment_comments(request, amendment_type, amendment_id):
    if amendment_type == 'modifier':
        amendment = get_object_or_404(models.ModifierAmendment,
                                      pk=amendment_id)
    elif amendment_type == 'additive':
        amendment = get_object_or_404(models.AdditiveAmendment,
                                      pk=amendment_id)
    elif amendment_type == 'supress':
        amendment = get_object_or_404(models.SupressAmendment,
                                      pk=amendment_id)
    html = render_to_string('amendments/_comments.html',
                            {'request': request, 'amendment': amendment})
    return JsonResponse({'html': html})


def render_segment_comments(request, segment_id):
    segment = get_object_or_404(models.BillSegment, pk=segment_id)
    html = render_to_string('segment/_comments.html', {'request': request,
                                                       'segment': segment})
    return JsonResponse({'html': html})


def create_comment(model, segment_id, request):
    ctype = ContentType.objects.get_for_model(model)
    segment = get_object_or_404(model, pk=segment_id)
    comment = models.Comment.objects.create(
        content_type=ctype,
        object_id=segment.id,
        text=request.POST.get('comment'),
        author=request.user
    )
    html = render_to_string('segment/_comment.html',
                            {'request': request, 'comment': comment})
    return JsonResponse({'html': html})


def create_vote(model, segment_id, request):
    ctype = ContentType.objects.get_for_model(model)
    segment = get_object_or_404(model, pk=segment_id)

    if issubclass(model, model_mixins.SegmentMixin):
        bill_is_closed = segment.bill_is_closed()
    else:
        bill_is_closed = segment.status == 'closed'

    if not bill_is_closed:
        new_vote = strtobool(request.POST.get('vote'))
        vote, created = models.UpDownVote.objects.get_or_create(
            defaults=dict(vote=new_vote),
            content_type=ctype,
            object_id=segment.id,
            user=request.user
        )
        if not created:
            if vote.vote == new_vote:
                vote.delete()
            else:
                vote.vote = new_vote
                vote.save()

        segment.refresh_from_db()
        html = render_to_string('segment/_votes.html', {'request': request,
                                                        'segment': segment})
        return JsonResponse({'html': html})
    else:
        return JsonResponse(
            {'title': _('Oops'),
             'message': _('This bill is closed for participation :(')},
            status=403
        )


def render_new_comment(request, segment_id, segment_type):
    if request.user.is_authenticated() and request.method == 'POST':
        if segment_type == 'segment':
            return create_comment(models.BillSegment, segment_id, request)
        if segment_type == 'modifier':
            return create_comment(models.ModifierAmendment,
                                  segment_id, request)
        if segment_type == 'supress':
            return create_comment(models.SupressAmendment, segment_id, request)
        if segment_type == 'additive':
            return create_comment(models.AdditiveAmendment,
                                  segment_id, request)
    else:
        return JsonResponse(
            {'title': _('Oops'),
             'message': _('You must be logged to comment :(')},
            status=403
        )


def render_votes(request, segment_id, segment_type):
    if request.user.is_authenticated() and request.method == 'POST':
        if segment_type == 'segment':
            return create_vote(models.BillSegment, segment_id, request)
        if segment_type == 'modifier':
            return create_vote(models.ModifierAmendment,
                               segment_id, request)
        if segment_type == 'supress':
            return create_vote(models.SupressAmendment, segment_id, request)
        if segment_type == 'additive':
            return create_vote(models.AdditiveAmendment,
                               segment_id, request)
        if segment_type == 'bill':
            return create_vote(models.Bill, segment_id, request)
    else:
        return JsonResponse(
            {'title': _('Oops'),
             'message': _('You must be logged to vote :(')},
            status=403
        )


def render_new_amendment(request, segment_id, amendment_type):
    if request.user.is_authenticated() and request.method == 'POST':
        segment = get_object_or_404(models.BillSegment, pk=segment_id)
        if amendment_type == 'modifier':
            amendment = models.ModifierAmendment.objects.create(
                content=request.POST.get('content'),
                replaced=segment,
                author=request.user,
            )

        if amendment_type == 'supress':
            amendment = models.SupressAmendment.objects.create(
                content=request.POST.get('content'),
                supressed=segment,
                author=request.user,
            )

        if amendment_type == 'additive':
            segment_type = models.SegmentType.objects.get(
                pk=request.POST.get('segment_type')
            )
            amendment = models.AdditiveAmendment.objects.create(
                content=request.POST.get('content'),
                segment_type=segment_type,
                reference=segment,
                author=request.user,
            )

        if 'amendment' in locals():
            html = render_to_string('amendments/_item.html',
                                    {'amendment_type': amendment_type,
                                     'amendment': amendment,
                                     'request': request})
            return JsonResponse({'html': html})

    else:
        return JsonResponse(
            {'title': _('Oops'),
             'message': _('You must be logged to suggest new amendment :(')},
            status=403
        )


class BillReportView(DetailView):
    model = models.Bill
    template_name = 'report/bill_report.html'

    def get_object(self, queryset=None):
        obj = super(BillReportView, self).get_object(queryset)
        if obj.status == 'draft':
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        context = super(BillReportView, self).get_context_data(**kwargs)
        domain = Site.objects.get_current().domain
        if settings.FORCE_SCRIPT_NAME:
            context['domain'] = domain + settings.FORCE_SCRIPT_NAME
        else:
            context['domain'] = domain
        segment_ctype = ContentType.objects.get_for_model(
            models.BillSegment)
        modifier_ctype = ContentType.objects.get_for_model(
            models.ModifierAmendment)
        additive_ctype = ContentType.objects.get_for_model(
            models.AdditiveAmendment)
        supress_ctype = ContentType.objects.get_for_model(
            models.SupressAmendment)
        bill_ctype = ContentType.objects.get_for_model(
            models.Bill)
        segments_ids = set(self.object.segments.values_list('id', flat=True))
        modifiers = models.ModifierAmendment.objects.filter(
            replaced__in=segments_ids)
        additives = models.AdditiveAmendment.objects.filter(
            reference__in=segments_ids)
        supressed = models.SupressAmendment.objects.filter(
            supressed__in=segments_ids)
        segments_votes = models.UpDownVote.objects.filter(
            content_type=segment_ctype, object_id__in=segments_ids)
        modifiers_votes = models.UpDownVote.objects.filter(
            content_type=modifier_ctype,
            object_id__in=modifiers.values_list('id', flat=True))
        additives_votes = models.UpDownVote.objects.filter(
            content_type=additive_ctype,
            object_id__in=additives.values_list('id', flat=True))
        supressed_votes = models.UpDownVote.objects.filter(
            content_type=supress_ctype,
            object_id__in=supressed.values_list('id', flat=True))
        bill_votes = models.UpDownVote.objects.filter(
            content_type=bill_ctype, object_id=self.object.id)
        segments_comments = models.Comment.objects.filter(
            content_type=segment_ctype, object_id__in=segments_ids)
        modifiers_comments = models.Comment.objects.filter(
            content_type=modifier_ctype,
            object_id__in=modifiers.values_list('id', flat=True))
        additives_comments = models.Comment.objects.filter(
            content_type=additive_ctype,
            object_id__in=additives.values_list('id', flat=True))
        supressed_comments = models.Comment.objects.filter(
            content_type=supress_ctype,
            object_id__in=supressed.values_list('id', flat=True))
        context['votes'] = (segments_votes.count() +
                            modifiers_votes.count() +
                            additives_votes.count() +
                            supressed_votes.count())
        context['comments'] = (segments_comments.count() +
                               modifiers_comments.count() +
                               additives_comments.count() +
                               supressed_comments.count())
        context['attendees'] = len(set(
            list(bill_votes.values_list('user__id', flat=True)) +
            list(segments_votes.values_list('user__id', flat=True)) +
            list(modifiers_votes.values_list('user__id', flat=True)) +
            list(additives_votes.values_list('user__id', flat=True)) +
            list(supressed_votes.values_list('user__id', flat=True)) +
            list(modifiers.values_list('author__id', flat=True)) +
            list(additives.values_list('author__id', flat=True)) +
            list(supressed.values_list('author__id', flat=True)) +
            list(segments_comments.values_list('author__id', flat=True)) +
            list(modifiers_comments.values_list('author__id', flat=True)) +
            list(additives_comments.values_list('author__id', flat=True)) +
            list(supressed_comments.values_list('author__id', flat=True))))
        context['segments_with_participation'] = self.object.segments.filter(
            ~Q(participation_count=0))
        return context

    def get_queryset(self):
        bill = models.Bill.objects.get(pk=self.kwargs.get('pk', None))
        if bill.allowed_users.all():
            if self.request.user in bill.allowed_users.all():
                return models.Bill.objects.filter(
                    pk=self.kwargs.get('pk', None))
            else:
                raise Http404()
        else:
            return self.model._default_manager.all()
