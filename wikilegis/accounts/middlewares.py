from django.contrib.auth.middleware import RemoteUserMiddleware
from django.contrib.auth import get_user_model
from django.contrib import auth
from django.contrib.auth import load_backend
from django.contrib.auth.backends import RemoteUserBackend
from django.core.exceptions import ImproperlyConfigured

User = get_user_model()


class WikilegisRemoteUser(RemoteUserMiddleware):
    header = "HTTP_AUTH_USER"

    # Override process request to pass the request to authentication method
    def process_request(self, request):
        # AuthenticationMiddleware is required so that request.user exists.
        if not hasattr(request, 'user'):
            raise ImproperlyConfigured(
                "The Django remote user auth middleware requires the"
                " authentication middleware to be installed.  Edit your"
                " MIDDLEWARE_CLASSES setting to insert"
                " 'django.contrib.auth.middleware.AuthenticationMiddleware'"
                " before the RemoteUserMiddleware class.")
        try:
            username = request.META[self.header]
        except KeyError:
            # If specified header doesn't exist then remove any existing
            # authenticated remote-user, or return (leaving request.user set to
            # AnonymousUser by the AuthenticationMiddleware).
            if request.user.is_authenticated():
                try:
                    stored_backend = load_backend(request.session.get(
                        auth.BACKEND_SESSION_KEY, ''))
                    if isinstance(stored_backend, RemoteUserBackend):
                        auth.logout(request)
                except ImproperlyConfigured:
                    # backend failed to load
                    auth.logout(request)
            return
        # If the user is already authenticated and that user is the user we are
        # getting passed in the headers, then the correct user is already
        # persisted in the session and we don't need to continue.
        if request.user.is_authenticated():
            cleaned_username = self.clean_username(username, request)
            if request.user.get_username() == cleaned_username:
                return
        # We are seeing this user for the first time in this session, attempt
        # to authenticate the user.
        user = auth.authenticate(remote_user=username, request=request)
        if user:
            # User is valid.  Set request.user and persist user in the session
            # by logging the user in.
            user.username = username
            user.save()

            request.user = user
            auth.login(request, user)
