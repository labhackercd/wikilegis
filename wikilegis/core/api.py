from django_comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework import parsers, renderers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from wikilegis import settings
from wikilegis.auth2.models import User
from wikilegis.core.models import Bill, BillSegment, TypeSegment, UpDownVote
from wikilegis.core.serializers import (BillSerializer, SegmentSerializer,
                                        CommentsSerializer, UserSerializer,
                                        TypeSegmentSerializer, BillDetailSerializer,
                                        CommentsSerializerForPost, SegmentSerializerForPost,
                                        VoteSerializer, UpDownVoteSerializerForPost,
                                        CreateUserSerializer)
from rest_framework import generics, permissions, mixins, filters
import django_filters
from django_filters import rest_framework


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


class TokenPermission(permissions.BasePermission):
    message = "Admin private token is mandatory to perform this action."

    def has_permission(self, request, view):
        if request.GET.get('api_key') == settings.API_KEY:
            return True
        else:
            return False


class BillAPI(generics.GenericAPIView, mixins.RetrieveModelMixin):
    serializer_class = BillDetailSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def get_object(self):
        obj = Bill.objects.get(pk=self.kwargs['pk'])
        return obj


class BillFilter(rest_framework.FilterSet):
    created = django_filters.DateTimeFilter(name="created", lookup_type="gte")
    modified = django_filters.DateTimeFilter(name="modified", lookup_type="gte")

    class Meta:
        model = Bill
        fields = ['theme', 'reporting_member', 'created', 'modified']


class BillListAPI(generics.ListAPIView):
    queryset = Bill.objects.exclude(status='draft').order_by('-created')
    serializer_class = BillSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = BillFilter
    search_fields = ('title', 'epigraph', 'description', 'theme')
    ordering_fields = ('closing_date', 'created', 'modified', 'id')


class CreateUserAPI(generics.CreateAPIView):
    serializer_class = CreateUserSerializer

    def create(self, request, *args, **kwargs):
        serialized = self.get_serializer(data=request.data)
        if serialized.is_valid():
            User.objects.create_user(
                email=serialized.data['email'],
                first_name=serialized.data['first_name'],
                last_name=serialized.data['last_name'],
                password=serialized.data['password']
            )
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)


class BillSegmentFilter(rest_framework.FilterSet):
    created = django_filters.DateTimeFilter(name="created", lookup_type="gte")
    modified = django_filters.DateTimeFilter(name="modified", lookup_type="gte")

    class Meta:
        model = BillSegment
        fields = ['bill', 'type', 'original', 'author', 'replaced', 'created', 'modified']


class SegmentsListAPI(generics.ListCreateAPIView):
    queryset = BillSegment.objects.exclude(bill__status='draft').order_by('-created')
    serializer_class = SegmentSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = BillSegmentFilter
    search_fields = ('number', 'content')
    ordering_fields = ('order', 'original', 'created', 'modified', 'id')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return self.serializer_class
        elif self.request.method == 'POST':
            return SegmentSerializerForPost

    def create(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            try:
                obj_replaced = BillSegment.objects.get(id=request.data['replaced'])
                obj = BillSegment()
                obj.bill_id = request.data['bill']
                obj.author = request.user
                obj.original = False
                obj.content = request.data['content']
                obj.replaced = obj_replaced
                obj.parent = obj_replaced.parent
                obj.number = obj_replaced.number
                obj.type = obj_replaced.type
                obj.save()
                return Response(status=201)
            except Exception as e:
                return Response(status=403, data=e.message)
        elif request.data['token']:
            token = Token.objects.get(key=request.data['token'])
            obj_replaced = BillSegment.objects.get(id=request.data['replaced'])
            obj = BillSegment()
            obj.bill_id = request.data['bill']
            obj.author = token.user
            obj.original = False
            obj.content = request.data['content']
            obj.replaced = obj_replaced
            obj.parent = obj_replaced.parent
            obj.number = obj_replaced.number
            obj.type = obj_replaced.type
            obj.save()
            serializer = SegmentSerializer(obj)
            return JSONResponse(serializer.data, status=201)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)


class CommentFilter(rest_framework.FilterSet):
    created = django_filters.DateTimeFilter(name="submit_date", lookup_type="gte")

    class Meta:
        model = Comment
        fields = ['content_type', 'object_pk', 'user']


class CommentListAPI(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentsSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = CommentFilter
    search_fields = ('comment', 'user_name')
    ordering_fields = ('submit_date', 'id')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return self.serializer_class
        elif self.request.method == 'POST':
            return CommentsSerializerForPost

    def create(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            obj_content_type = ContentType.objects.get_for_model(BillSegment)
            obj = Comment()
            obj.content_type = obj_content_type
            obj.user = request.user
            obj.comment = request.data['comment']
            obj.object_pk = request.data['object_pk']
            obj.site_id = settings.SITE_ID
            obj.save()
            return Response(status=201)
        elif request.data['token']:
            token = Token.objects.get(key=request.data['token'])
            obj_content_type = ContentType.objects.get_for_model(BillSegment)
            obj = Comment()
            obj.content_type = obj_content_type
            obj.user = token.user
            obj.comment = request.data['comment']
            obj.object_pk = request.data['object_id']
            obj.site_id = settings.SITE_ID
            obj.save()
            serializer = CommentsSerializer(obj)
            return JSONResponse(serializer.data, status=201)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)


class VotesFilter(rest_framework.FilterSet):
    created = django_filters.DateTimeFilter(name="created", lookup_type="gte")
    modified = django_filters.DateTimeFilter(name="modified", lookup_type="gte")

    class Meta:
        model = UpDownVote
        fields = ['user', 'object_id', 'vote', 'created', 'modified']


class UpDownVoteListAPI(generics.ListCreateAPIView):
    queryset = UpDownVote.objects.all()
    serializer_class = VoteSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    filter_class = VotesFilter
    ordering_fields = ('created', 'modified', 'id')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return self.serializer_class
        elif self.request.method == 'POST':
            return UpDownVoteSerializerForPost

    def get_queryset(self):
        queryset = self.queryset
        if self.request.user.is_authenticated():
            queryset = queryset.filter(user=self.request.user)
        return queryset

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            obj_content_type = ContentType.objects.get_for_model(BillSegment)
            vote = UpDownVote.objects.get_or_create(user=request.user,
                                                    object_id=request.data['object_id'],
                                                    content_type=obj_content_type)[0]
            vote.vote = eval(request.data['vote'])
            vote.save()
            return Response(status=201)
        elif request.data['token']:
            token = Token.objects.get(key=request.data['token'])
            obj_content_type = ContentType.objects.get_for_model(BillSegment)
            vote = UpDownVote.objects.get_or_create(user=token.user,
                                                    object_id=request.data['object_id'],
                                                    content_type=obj_content_type)[0]
            vote.vote = eval(request.data['vote'])
            vote.save()
            queryset = UpDownVote.objects.filter(object_id=request.data['object_id'],
                                                 content_type=obj_content_type)
            serializer = VoteSerializer(queryset, many=True)
            return JSONResponse(serializer.data, status=201)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)


class VoteUpdateDeleteAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = UpDownVote.objects.all()
    serializer_class = UpDownVoteSerializerForPost

    def put(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user.is_authenticated() and request.user == obj.user:
            return self.update(request, *args, **kwargs)
        elif request.data['token']:
            token = Token.objects.get(key=request.data['token'])
            if token.user == obj.user:
                return self.update(request, *args, **kwargs)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user.is_authenticated() and request.user == obj.user:
            return self.destroy(request, *args, **kwargs)
        elif request.data['token']:
            token = Token.objects.get(key=request.data['token'])
            if token.user == obj.user:
                return self.destroy(request, *args, **kwargs)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class TypeSegmentAPI(generics.ListAPIView):
    queryset = TypeSegment.objects.all()
    serializer_class = TypeSegmentSerializer


class UserAPI(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (TokenPermission, )


class UserUpdateAPI(generics.UpdateAPIView):
    model = User
    serializer_class = UserSerializer
    permission_classes = (TokenPermission, )

    def get_object(self, queryset=None):
        return self.model.objects.get(email=self.request.data['email'])

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        user.email = request.data.get('email', user.email)
        user.first_name = request.data.get('first_name', user.first_name)
        user.last_name = request.data.get('last_name', user.last_name)
        user.avatar = request.data.get('avatar', user.avatar)
        user.save()
        return Response(status=status.HTTP_202_ACCEPTED)


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'bills': reverse('bill_list_api',
                         request=request, format=format),
        'segments': reverse('segments_list_api',
                            request=request, format=format),
        'comments': reverse('comment_list_api',
                            request=request, format=format),
        'segment-types': reverse('types_segments_list_api',
                                 request=request, format=format),
        'users': reverse('users_list_api',
                         request=request, format=format),
        'votes': reverse('votes_api',
                         request=request, format=format)
    })


class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user_serializer = UserSerializer(user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user': user_serializer.data})
