from django.conf import settings
from django.conf.urls import url
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from api.authorization import UpdateUserAuthorization
from tastypie.resources import ModelResource, ALL_WITH_RELATIONS, ALL
from tastypie import fields

from core import models as core_models
from api import statistics


class UserResource(ModelResource):

    def dehydrate(self, bundle):
        bundle.data.pop('is_active', None)
        bundle.data.pop('is_staff', None)
        bundle.data.pop('is_superuser', None)

        bundle.data['votes_count'] = bundle.obj.updownvote_set.count()
        bundle.data['comments_count'] = bundle.obj.comment_set.count()
        bundle.data['additive_count'] = bundle.obj.additiveamendment_set.count()
        bundle.data['modifier_count'] = bundle.obj.modifieramendment_set.count()
        bundle.data['supress_count'] = bundle.obj.supressamendment_set.count()

        bill_count = 0
        for bill in core_models.Bill.objects.all():
            if bill.votes.filter(user=bundle.obj).count() > 0:
                bill_count += 1
                continue

            for segment in bill.segments.all():
                if segment.votes.filter(user=bundle.obj).count() > 0:
                    bill_count += 1
                    break

                if segment.comments.filter(author=bundle.obj).count() > 0:
                    bill_count += 1
                    break

                has_participation = False
                for amendment in segment.additive_amendments.all():
                    if amendment.author == bundle.obj:
                        has_participation = True
                        break
                    else:
                        if amendment.votes.filter(user=bundle.obj).count() > 0:
                            has_participation = True
                            break

                        if amendment.comments.filter(author=bundle.obj).count() > 0:
                            has_participation = True
                            break

                if has_participation:
                    bill_count += 1
                    break

                for amendment in segment.modifier_amendments.all():
                    if amendment.author == bundle.obj:
                        has_participation = True
                        break
                    else:
                        if amendment.votes.filter(user=bundle.obj).count() > 0:
                            has_participation = True
                            break

                        if amendment.comments.filter(author=bundle.obj).count() > 0:
                            has_participation = True
                            break

                if has_participation:
                    bill_count += 1
                    break

                for amendment in segment.supress_amendments.all():
                    if amendment.author == bundle.obj:
                        has_participation = True
                        break
                    else:
                        if amendment.votes.filter(user=bundle.obj).count() > 0:
                            has_participation = True
                            break

                        if amendment.comments.filter(author=bundle.obj).count() > 0:
                            has_participation = True
                            break

                if has_participation:
                    bill_count += 1
                    break
        bundle.data['bill_participations'] = bill_count

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

    def alter_list_data_to_serialize(self, request, data):
        segment_votes = 0
        amendment_votes = 0
        bill_votes = 0
        additive_count = 0
        supress_count = 0
        modifier_count = 0
        comments_count = 0
        participants_count = 0

        for bill in self.get_object_list(request):
            stats = statistics.bill_stats(bill)
            bill_votes += stats['bill_votes']
            additive_count += stats['additive_count']
            supress_count += stats['supress_count']
            modifier_count += stats['modifier_count']
            comments_count += stats['comments_count']
            segment_votes += stats['segment_votes']
            amendment_votes += stats['amendment_votes']
            participants_count += stats['participants_count']

        data['meta']['segment_votes'] = segment_votes
        data['meta']['amendment_votes'] = amendment_votes
        data['meta']['comments_count'] = comments_count
        data['meta']['bill_votes'] = bill_votes
        data['meta']['additive_count'] = additive_count
        data['meta']['supress_count'] = supress_count
        data['meta']['modifier_count'] = modifier_count
        data['meta']['amendments_count'] = (
            additive_count + supress_count + modifier_count
        )
        data['meta']['participants_count'] = participants_count
        return data

    def dehydrate(self, bundle):
        stats = statistics.bill_stats(bundle.obj)

        bundle.data['amendment_votes'] = stats['amendment_votes']
        bundle.data['segment_votes'] = stats['segment_votes']
        bundle.data['comments_count'] = stats['comments_count']
        bundle.data['additive_amendments_count'] = stats['additive_count']
        bundle.data['supress_amendments_count'] = stats['supress_count']
        bundle.data['modifier_amendments_count'] = stats['modifier_count']
        bundle.data['participants_count'] = stats['participants_count']
        return bundle

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
            'created': ALL,
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
        filtering = {
            'author': ALL_WITH_RELATIONS,
            'reference': ALL_WITH_RELATIONS,
            'id': ALL,
            'created': ['exact', 'lt', 'lte', 'gte', 'gt'],
            'modified': ['exact', 'lt', 'lte', 'gte', 'gt'],
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
        filtering = {
            'author': ALL_WITH_RELATIONS,
            'replaced': ALL_WITH_RELATIONS,
            'id': ALL,
            'created': ['exact', 'lt', 'lte', 'gte', 'gt'],
            'modified': ['exact', 'lt', 'lte', 'gte', 'gt'],
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
        filtering = {
            'author': ALL_WITH_RELATIONS,
            'supressed': ALL_WITH_RELATIONS,
            'id': ALL,
            'created': ['exact', 'lt', 'lte', 'gte', 'gt'],
            'modified': ['exact', 'lt', 'lte', 'gte', 'gt'],
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
            'created': ['exact', 'lt', 'lte', 'gte', 'gt'],
            'modified': ['exact', 'lt', 'lte', 'gte', 'gt'],
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
            'created': ['exact', 'lt', 'lte', 'gte', 'gt'],
            'modified': ['exact', 'lt', 'lte', 'gte', 'gt'],
        }
