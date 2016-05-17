from django.utils.text import slugify
from django_comments.models import Comment
from rest_framework import serializers

from wikilegis.core.models import Bill
from wikilegis.core.models import BillSegment


class SegmentSerializer(serializers.ModelSerializer):
    parent = serializers.SerializerMethodField('get_parent_name')
    type = serializers.SerializerMethodField('get_type_name')

    class Meta(object):
        model = BillSegment
        fields = ('id', 'bill', 'original', 'replaced', 'parent', 'type', 'number', 'content')

    def get_parent_name(self, obj):
        if obj.parent:
            if obj.parent.number:
                if obj.parent.number == '0':
                    return slugify(obj.parent.type.name)
                else:
                    return '{kind} {number}'.format(
                        kind=slugify(obj.parent.type.name), number=obj.parent.number)
            else:
                return obj.parent

    def get_type_name(self, obj):
        return slugify(obj.type.name)


class BillSegmentSerializer(serializers.ModelSerializer):
    queryset = BillSegment.objects.filter(original=True)
    parent = serializers.SerializerMethodField('get_parent_name')
    type = serializers.SerializerMethodField('get_type_name')

    class Meta(object):
        model = BillSegment
        fields = ('id', 'parent', 'type', 'number', 'content')

    def get_parent_name(self, obj):
        if obj.parent:
            if obj.parent.number:
                if obj.parent.number == '0':
                    return slugify(obj.parent.type.name)
                else:
                    return '{kind} {number}'.format(
                        kind=slugify(obj.parent.type.name), number=obj.parent.number)
            else:
                return obj.parent

    def get_type_name(self, obj):
        return slugify(obj.type.name)


class BillSerializer(serializers.ModelSerializer):
    segments = BillSegmentSerializer(many=True, read_only=True)

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
