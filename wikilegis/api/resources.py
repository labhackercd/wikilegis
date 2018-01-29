from django.conf import settings
from django.conf.urls import url
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from api.authorization import UpdateUserAuthorization
from tastypie.resources import ModelResource, ALL_WITH_RELATIONS, ALL
from tastypie import fields

from core import models as core_models


class UserResource(ModelResource):

    def dehydrate(self, bundle):
        bundle.data.pop('is_active', None)
        bundle.data.pop('is_staff', None)
        bundle.data.pop('is_superuser', None)

        key = bundle.request.GET.get('api_key', None)
        if key != settings.API_KEY:
            del bundle.data['email']
        return bundle

    def prepend_urls(self):
        re_url = r"^(?P<resource_name>%s)/(?P<username>[\w\d_.-]+)/$".format(
            self._meta.resource_name
        )
        return [
            url(re_url, self.wrap_view('dispatch_detail'),
                name="api_dispatch_detail"),
        ]

    class Meta:
        queryset = get_user_model().objects.all()
        allowed_methods = ['get', 'put', 'delete']
        excludes = ['last_login', 'password', 'date_joined']
        authorization = UpdateUserAuthorization()
        detail_uri_name = 'username'
        filtering = {
            'first_name': ALL,
            'last_name': ALL,
            'username': ALL,
        }


class BillThemeResource(ModelResource):
    class Meta:
        queryset = core_models.BillTheme.objects.all()
        allowed_methods = ['get']
        filtering = {
            'slug': ALL,
            'description': ALL
        }


class BillVideoResource(ModelResource):

    class Meta:
        queryset = core_models.BillVideo.objects.all()
        allowed_methods = ['get']


class BillReferenceResource(ModelResource):

    class Meta:
        queryset = core_models.BillReference.objects.all()
        allowed_methods = ['get']


class BillResource(ModelResource):
    theme = fields.ForeignKey(BillThemeResource, 'theme', full=True)
    allowed_users = fields.ToManyField(UserResource, 'allowed_users',
                                       full=True)
    videos = fields.ToManyField(BillVideoResource, 'videos', full=True,
                                null=True)
    references = fields.ToManyField(BillReferenceResource, 'references',
                                    full=True, null=True)
    comments = fields.ToManyField('api.resources.CommentResource', 'comments')
    votes = fields.ToManyField('api.resources.UpDownVoteResource', 'votes')

    class Meta:
        queryset = core_models.Bill.objects.filter(
            allowed_users__isnull=True,
            is_visible=True).exclude(status='draft').order_by(
            '-status', '-modified')
        resource_name = 'bill'
        excludes = ['is_visible']
        allowed_methods = ['get']
        filtering = {
            'theme': ALL_WITH_RELATIONS,
            'title': ALL,
            'status': ALL,
            'id': ALL,
            'closing_date': ALL,
        }
        ordering = ['closing_date', 'status', 'modified']


class SegmentTypeResource(ModelResource):
    parents = fields.ToManyField('self', 'parents', null=True)

    class Meta:
        queryset = core_models.SegmentType.objects.all()
        allowed_methods = ['get']


class BillSegmentResource(ModelResource):
    segment_type = fields.ForeignKey(SegmentTypeResource, 'segment_type',
                                     full=True, null=True)
    parent = fields.ForeignKey('self', 'parent', full=True, null=True)
    bill = fields.ForeignKey(BillResource, 'bill', full=True)
    comments = fields.ToManyField('api.resources.CommentResource', 'comments')
    votes = fields.ToManyField('api.resources.UpDownVoteResource', 'votes')

    class Meta:
        queryset = core_models.BillSegment.objects.exclude(
            bill__status='draft'
        ).exclude(
            bill__is_visible=False).exclude(bill__allowed_users__isnull=False)
        allowed_methods = ['get']
        excludes = ['modified']
        filtering = {
            'bill': ALL_WITH_RELATIONS,
            'id': ALL,
        }


class AdditiveAmendmentResource(ModelResource):
    author = fields.ForeignKey(UserResource, 'author', full=True)
    reference = fields.ForeignKey(BillSegmentResource, 'reference', full=True)
    segment_type = fields.ForeignKey(SegmentTypeResource, 'segment_type',
                                     full=True, null=True)
    comments = fields.ToManyField('api.resources.CommentResource', 'comments')
    votes = fields.ToManyField('api.resources.UpDownVoteResource', 'votes')

    class Meta:
        queryset = core_models.AdditiveAmendment.objects.exclude(
            reference__bill__status='draft'
        ).exclude(reference__bill__is_visible=False)
        allowed_methods = ['get']
        excludes = ['modified']
        filtering = {
            'author': ALL_WITH_RELATIONS,
            'reference': ALL_WITH_RELATIONS,
            'id': ALL,
        }


class ModifierAmendmentResource(ModelResource):
    author = fields.ForeignKey(UserResource, 'author', full=True)
    replaced = fields.ForeignKey(BillSegmentResource, 'replaced', full=True)
    segment_type = fields.ForeignKey(SegmentTypeResource, 'segment_type',
                                     full=True, null=True)
    comments = fields.ToManyField('api.resources.CommentResource', 'comments')
    votes = fields.ToManyField('api.resources.UpDownVoteResource', 'votes')

    class Meta:
        queryset = core_models.ModifierAmendment.objects.exclude(
            replaced__bill__status='draft'
        ).exclude(replaced__bill__is_visible=False)
        allowed_methods = ['get']
        excludes = ['modified']
        filtering = {
            'author': ALL_WITH_RELATIONS,
            'replaced': ALL_WITH_RELATIONS,
            'id': ALL,
        }


class SupressAmendmentResource(ModelResource):
    author = fields.ForeignKey(UserResource, 'author', full=True)
    supressed = fields.ForeignKey(BillSegmentResource, 'supressed', full=True)
    segment_type = fields.ForeignKey(SegmentTypeResource, 'segment_type',
                                     full=True, null=True)
    comments = fields.ToManyField('api.resources.CommentResource', 'comments')
    votes = fields.ToManyField('api.resources.UpDownVoteResource', 'votes')

    class Meta:
        queryset = core_models.SupressAmendment.objects.exclude(
            supressed__bill__status='draft'
        ).exclude(supressed__bill__is_visible=False)
        allowed_methods = ['get']
        excludes = ['modified']
        filtering = {
            'author': ALL_WITH_RELATIONS,
            'supressed': ALL_WITH_RELATIONS,
            'id': ALL,
        }


class ContentTypeResource(ModelResource):

    class Meta:
        queryset = ContentType.objects.all()


class UpDownVoteResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user', full=True)
    content_type = fields.ForeignKey(ContentTypeResource, 'content_type')

    def dehydrate_content_type(self, bundle):
        return bundle.obj.content_type.name

    class Meta:
        queryset = core_models.UpDownVote.objects.all()
        resource_name = 'vote'
        allowed_methods = ['get']
        filtering = {
            'author': ALL_WITH_RELATIONS,
            'vote': ALL,
            'id': ALL,
        }


class CommentResource(ModelResource):
    author = fields.ForeignKey(UserResource, 'author', full=True)
    content_type = fields.ForeignKey(ContentTypeResource, 'content_type')

    def dehydrate_content_type(self, bundle):
        return bundle.obj.content_type.name

    class Meta:
        queryset = core_models.Comment.objects.all()
        allowed_methods = ['get']
        filtering = {
            'author': ALL_WITH_RELATIONS,
            'id': ALL,
        }
