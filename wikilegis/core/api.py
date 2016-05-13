from django_comments.models import Comment

from wikilegis.core.models import Bill, BillSegment
from wikilegis.core.serializers import BillSerializer, SegmentSerializer, CommentsSerializer
from rest_framework import generics


class BillListAPI(generics.ListAPIView):
    queryset = Bill.objects.exclude(status='draft').order_by('-created')
    serializer_class = BillSerializer


class SegmentsListAPI(generics.ListAPIView):
    queryset = BillSegment.objects.exclude(bill__status='draft').order_by('-created')
    serializer_class = SegmentSerializer


class CommentListAPI(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentsSerializer
