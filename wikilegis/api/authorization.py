from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized
from django.conf import settings


class UpdateUserAuthorization(Authorization):

    def api_key_is_valid(self, bundle):
        api_key = bundle.request.GET.get('api_key', None)
        if api_key and api_key == settings.API_KEY:
            return True
        else:
            raise Unauthorized('Missing api key')

    def update_list(self, object_list, bundle):
        raise Unauthorized('You cannot perform this action')

    def update_detail(self, object_list, bundle):
        return self.api_key_is_valid(bundle)

    def delete_list(self, object_list, bundle):
        raise Unauthorized('You cannot perform this action')

    def delete_detail(self, object_list, bundle):
        return self.api_key_is_valid(bundle)
