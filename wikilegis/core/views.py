from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.views.generic.base import TemplateView

from core import models


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['bills'] = models.Bill.objects.exclude(
            status='draft', is_visible=False).order_by('-created')
        return context


def render_bill_info(request, bill_id):
    bill = get_object_or_404(models.Bill, pk=bill_id)
    html = render_to_string('bill/_info.html', {'bill': bill})
    return JsonResponse({'html': html})


def render_bill_content(request, bill_id):
    bill = get_object_or_404(models.Bill, pk=bill_id)
    html = render_to_string('bill/_content.html', {'bill': bill})
    return JsonResponse({'html': html})


def render_bill_amendments(request, segment_id):
    segment = get_object_or_404(models.BillSegment, pk=segment_id)
    html = render_to_string('amendments/_index.html', {'segment': segment})
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
                            {'amendment': amendment})
    return JsonResponse({'html': html})


def render_segment_comments(request, segment_id):
    segment = get_object_or_404(models.BillSegment, pk=segment_id)
    html = render_to_string('segment/_comments.html', {'segment': segment})
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
                            {'comment': comment})
    return JsonResponse({'html': html})


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
