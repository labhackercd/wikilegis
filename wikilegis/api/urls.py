from django.conf.urls import url, include
from tastypie.api import Api
from api import resources

v1_api = Api(api_name='v1')
v1_api.register(resources.UserResource())
v1_api.register(resources.BillThemeResource())
v1_api.register(resources.CommentResource())
v1_api.register(resources.BillResource())
v1_api.register(resources.BillVideoResource())
v1_api.register(resources.BillReferenceResource())
v1_api.register(resources.SegmentTypeResource())
v1_api.register(resources.BillSegmentResource())
v1_api.register(resources.AdditiveAmendmentResource())
v1_api.register(resources.ModifierAmendmentResource())
v1_api.register(resources.SupressAmendmentResource())
v1_api.register(resources.UpDownVoteResource())

urlpatterns = [
    url(r'^api/', include(v1_api.urls)),
]
