from django.http import JsonResponse
from django.template.loader import render_to_string


def render_bill_info(request, bill_id):
    html = render_to_string('bill/_info.html')
    return JsonResponse({'html': html})


def render_bill_content(request, bill_id):
    html = render_to_string('bill/_content.html')
    return JsonResponse({'html': html})


def render_bill_interactions(request, segment_id):
    html = render_to_string('bill/_interactions.html')
    return JsonResponse({'html': html})


def render_segment_comments(request, segment_id):
    html = render_to_string('segment/_comments.html')
    return JsonResponse({'html': html})
