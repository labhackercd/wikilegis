from django.conf import settings
from django.contrib.auth import get_user_model
from tastypie.resources import ModelResource, ALL_WITH_RELATIONS, ALL
from tastypie import fields

from core import models as core_models


class UserResource(ModelResource):

    def dehydrate_email(self, bundle):
        key = bundle.request.GET.get('api_key', None)
        if key == settings.API_KEY:
            return bundle.data['email']
        else:
            return None

    class Meta:
        queryset = get_user_model().objects.all()
        allowed_methods = ['get']
        excludes = ['is_active', 'is_staff', 'is_superuser', 'last_login',
                    'password', 'date_joined']
        filtering = {
            'first_name': ALL,
            'last_name': ALL,
            'username': ALL
        }


class BillThemeResource(ModelResource):
    class Meta:
        queryset = core_models.BillTheme.objects.all()
        allowed_methods = ['get']
        filtering = {
            'slug': ALL,
            'description': ALL
        }


class CommentResource(ModelResource):
    author = fields.ForeignKey(UserResource, 'author', full=True)

    class Meta:
        queryset = core_models.Comment.objects.all()
        allowed_methods = ['get']
        filtering = {
            'author': ALL_WITH_RELATIONS
        }


class BillVideoResource(ModelResource):

    class Meta:
        queryset = core_models.BillVideo.objects.all()
        allowed_methods = ['get']
        excludes = ['resource_uri', ]


class BillResource(ModelResource):
    theme = fields.ForeignKey(BillThemeResource, 'theme', full=True)
    allowed_users = fields.ToManyField(UserResource, 'allowed_users',
                                       full=True)
    reporting_member = fields.ForeignKey(UserResource, 'reporting_member',
                                         full=True, null=True)
    comments = fields.ToManyField(CommentResource, 'comments',
                                  full=True)
    videos = fields.ToManyField(BillVideoResource, 'videos', full=True,
                                null=True)

    def dehydrate_comments(self, bundle):
        return_data = []
        for comment in bundle.data['comments']:
            return_data.append(comment.id)
        return return_data

    class Meta:
        queryset = core_models.Bill.objects.exclude(
            status='draft'
        ).exclude(is_visible=False)
        excludes = ['is_visible']
        allowed_methods = ['get']
