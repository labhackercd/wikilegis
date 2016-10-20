from django_comments.models import Comment
from django.conf import settings
from rest_framework import serializers

from wikilegis.auth2.models import User
from wikilegis.core.models import Bill, BillSegment, TypeSegment, UpDownVote


class BasicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'avatar')


class CommentsSerializer(serializers.ModelSerializer):
    content_type = serializers.SerializerMethodField('get_content_type_name')
    user = BasicUserSerializer()

    def __init__(self, *args, **kwargs):
        super(CommentsSerializer, self).__init__(*args, **kwargs)

        try:
            request = kwargs.get('context').get('request')
            api_key = request.GET.get('api_key', None)

            if api_key and api_key == settings.API_KEY:
                self.fields['user'] = UserSerializer()
            else:
                self.fields['user'] = BasicUserSerializer()
        except AttributeError:
            # When django initializes kwarg is None
            pass

    def get_content_type_name(self, obj):
        return obj.content_type.name

    class Meta:
        model = Comment
        fields = ('id', 'user', 'submit_date',
                  'content_type', 'object_pk', 'comment')


class CommentsSerializerForPost(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('object_pk', 'comment')


class VoteSerializer(serializers.ModelSerializer):
    content_type = serializers.SerializerMethodField('get_content_type_name')
    user = BasicUserSerializer()

    def get_content_type_name(self, obj):
        return obj.content_type.name

    class Meta:
        model = UpDownVote
        fields = ('id', 'user', 'content_type', 'object_id', 'vote', 'created', 'modified')


class SegmentSerializer(serializers.ModelSerializer):
    author = BasicUserSerializer()
    comments = CommentsSerializer(many=True)
    votes = VoteSerializer(many=True)

    def __init__(self, *args, **kwargs):
        super(SegmentSerializer, self).__init__(*args, **kwargs)

        try:
            request = kwargs.get('context').get('request')
            api_key = request.GET.get('api_key', None)

            if api_key and api_key == settings.API_KEY:
                self.fields['author'] = UserSerializer()
            else:
                self.fields['author'] = BasicUserSerializer()
        except AttributeError:
            # When django initializes kwarg is None
            pass

    class Meta:
        model = BillSegment
        fields = ('id', 'order', 'bill', 'original', 'replaced', 'parent',
                  'type', 'number', 'content', 'author', 'comments', 'votes',
                  'created', 'modified')


class SegmentSerializerForPost(serializers.ModelSerializer):
    bill = serializers.UUIDField()
    replaced = serializers.UUIDField()

    class Meta:
        model = BillSegment
        fields = ('bill', 'replaced', 'content')


class BillDetailSerializer(serializers.ModelSerializer):
    segments = SegmentSerializer(many=True)

    class Meta:
        model = Bill
        fields = ('id', 'title', 'epigraph', 'description', 'closing_date',
                  'status', 'theme', 'segments', 'created', 'modified')


class BillSerializer(serializers.ModelSerializer):
    reporting_member = BasicUserSerializer()
    proposals_count = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super(BillSerializer, self).__init__(*args, **kwargs)

        try:
            request = kwargs.get('context').get('request')
            api_key = request.GET.get('api_key', None)

            if api_key and api_key == settings.API_KEY:
                self.fields['reporting_member'] = UserSerializer()
            else:
                self.fields['reporting_member'] = BasicUserSerializer()
        except AttributeError:
            # When django initializes kwarg is None
            pass

    class Meta:
        model = Bill
        fields = ('id', 'title', 'epigraph', 'description', 'reporting_member',
                  'status', 'theme', 'proposals_count', 'segments', 'created',
                  'modified', 'closing_date')

    def get_proposals_count(self, obj):
        return obj.segments.filter(original=False).count()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'avatar')


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password')
        write_only_fields = ('password',)


class TypeSegmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeSegment
        fields = ('id', 'name')


class UpDownVoteSerializerForPost(serializers.ModelSerializer):
    class Meta:
        model = UpDownVote
        fields = ('object_id', 'vote')
