from django.conf import settings
from django.conf.urls import url, include
from registration.backends.default.views import RegistrationView
from registration.backends.simple.views import RegistrationView as SimpleRegistrationView
from wikilegis.auth2.views import ActivationCompleteView
from rest_framework.authtoken import views

urlpatterns = [
    # XXX We want the user to be redirected after successful account activation.
    # So we override the `registration_activation_complete` view to do the redirect.
    # Note that tt overrides the included view from `registration.backends.default`
    # and should always come before its inclusion or else little cutie puppies will cry.
    url(r'^activate/complete/$', ActivationCompleteView.as_view(),
        name='registration_activation_complete'),
    url(r'^activate/resend/$', 'wikilegis.auth2.views.resend_activation', name='resend_activation'),
    url(r'^', include('registration.backends.default.urls')),
]


if getattr(settings, 'ACCOUNT_ACTIVATION_REQUIRED', True):
    registration_view = RegistrationView
else:
    registration_view = SimpleRegistrationView

urlpatterns += [
    url(r'^register/$', registration_view.as_view(), name='registration_register'),
    # TODO all these names sucks (edit, your_profile, edit_profile). pls fix.
    url(r'^edit/$', 'wikilegis.auth2.views.your_profile', name='edit_profile'),
    url(r'^users/(?P<user_id>\d+)/$', 'wikilegis.auth2.views.show_users_profile', name='users_profile'),
]


urlpatterns += [
    url(r'^api-token-auth/', views.obtain_auth_token)
]
