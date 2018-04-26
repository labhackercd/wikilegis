from django.contrib.auth.backends import RemoteUserBackend
from django.contrib.auth import get_user_model
import json
UserModel = get_user_model()


class WikilegisAuthBackend(RemoteUserBackend):

    def authenticate(self, remote_user, request=None):
        if not remote_user:
            return
        user = None
        remote_user_data = json.loads(
            request.META.get('HTTP_REMOTE_USER_DATA')
        )
        user, created = UserModel.objects.get_or_create(
            email=remote_user_data.get('email'),
        )

        if created:
            user.first_name = remote_user_data['first_name']
            user.last_name = remote_user_data['last_name']

        return user
