from django_comments.models import Comment
from rest_framework import serializers

from wikilegis.auth2.models import User
from wikilegis.core.models import Bill
from wikilegis.core.models import BillSegment


class SegmentSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = BillSegment
        fields = ('id', 'bill', 'original', 'replaced', 'parent',
                  'type', 'number', 'content')


class BillSegmentSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = BillSegment
        fields = ('id', 'parent', 'type', 'number', 'content')


class BillSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Bill
        fields = ('id',
                  'title',
                  'epigraph',
                  'description',
                  'status',
                  'theme',
                  'segments')


class CommentsSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Comment
        fields = ('id',
                  'user',
                  'user_name',
                  'user_email',
                  'submit_date',
                  'content_type',
                  'object_pk',
                  'comment')


class UserSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = User
        fields = ('email', 'first_name', 'last_name', 'avatar')
