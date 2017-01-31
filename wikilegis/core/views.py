from django.http import JsonResponse
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
    html = render_to_string('bill/_amendments.html', {'segment': segment})
    return JsonResponse({'html': html})


def render_segment_comments(request, segment_id):
    segment = get_object_or_404(models.BillSegment, pk=segment_id)
    html = render_to_string('segment/_comments.html', {'segment': segment})
    return JsonResponse({'html': html})
