from django_comments.models import Comment
from rest_framework import serializers

from wikilegis.auth2.models import User
from wikilegis.core.models import Bill, BillSegment, TypeSegment


class SegmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = BillSegment
        fields = ('id', 'bill', 'original', 'replaced', 'parent',
                  'type', 'number', 'content')


class BillSegmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = BillSegment
        fields = ('id', 'parent', 'type', 'number', 'content')


class BillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bill
        fields = ('id', 'title', 'epigraph', 'description',
                  'status', 'theme', 'segments')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'avatar')


class CommentsUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'avatar')


class CommentsSerializer(serializers.ModelSerializer):
    content_type = serializers.SerializerMethodField('get_content_type_name')
    user = CommentsUserSerializer()

    def get_content_type_name(self, obj):
        return obj.content_type.name

    class Meta:
        model = Comment
        fields = ('id', 'user', 'submit_date',
                  'content_type', 'object_pk', 'comment')


class TypeSegmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeSegment
        fields = ('id', 'name')
