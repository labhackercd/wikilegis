from django.http import JsonResponse


def render_bill_info(request, bill_id):
    html = render_to_string('bill_info.html')
    return JsonResponse({'html': html})

def render_bill_content(request, bill_id):
    html = render_to_string('bill_content.html')
    return JsonResponse({'html': html})

def render_bill_interactions(request, segment_id):
    html = render_to_string('bill_interactions.html')
    return JsonResponse({'html': html})
