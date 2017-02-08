from django.conf.urls import url, include
from tastypie.api import Api
from api import resources

v1_api = Api(api_name='v1')
v1_api.register(resources.UserResource())
v1_api.register(resources.BillThemeResource())
v1_api.register(resources.CommentResource())
v1_api.register(resources.BillResource())
v1_api.register(resources.BillVideoResource())

urlpatterns = [
    url(r'^api/', include(v1_api.urls)),
]
