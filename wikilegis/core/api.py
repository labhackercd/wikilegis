from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django_comments.models import Comment
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import status

from wikilegis import settings
from wikilegis.auth2.models import User
from wikilegis.core.models import Bill, BillSegment
from wikilegis.core.serializers import BillSerializer, SegmentSerializer, CommentsSerializer, UserSerializer
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


class UserUpdateAPI(generics.UpdateAPIView):
    model = User
    serializer_class = UserSerializer

    def get_object(self, queryset=None):
        return self.model.objects.get(email=self.request.data['email'])

    def put(self, request, *args, **kwargs):
        if self.request.data.get('api_key') == settings.API_KEY:
            user = self.get_object()
            user.email = request.data.get('email', user.email)
            user.first_name = request.data.get('first_name', user.first_name)
            user.last_name = request.data.get('last_name', user.last_name)
            user.avatar = request.data.get('avatar', user.avatar)
            user.save()
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'bills': reverse('bill_list_api', request=request, format=format),
        'segments': reverse('segments_list_api', request=request, format=format),
        'comments': reverse('comment_list_api', request=request, format=format)
    })