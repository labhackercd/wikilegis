from django_comments.models import Comment
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse

from wikilegis.core.models import Bill
from wikilegis.core.models import BillSegment
from wikilegis.core.serializers import BillSerializer
from wikilegis.core.serializers import CommentsSerializer
from wikilegis.core.serializers import SegmentSerializer


class BillListAPI(generics.ListAPIView):
    queryset = Bill.objects.exclude(status='draft').order_by('-created')
    serializer_class = BillSerializer


class SegmentsListAPI(generics.ListAPIView):
    queryset = BillSegment.objects.exclude(bill__status='draft').order_by('-created')
    serializer_class = SegmentSerializer


class CommentListAPI(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentsSerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'bills': reverse('bill_list_api', request=request, format=format),
        'segments': reverse('segments_list_api', request=request, format=format),
        'comments': reverse('comment_list_api', request=request, format=format)
    })
