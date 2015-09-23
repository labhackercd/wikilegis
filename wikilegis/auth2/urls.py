from django.conf import settings
from django.conf.urls import url, include
from registration.backends.default.views import RegistrationView
from registration.backends.simple.views import RegistrationView as SimpleRegistrationView

urlpatterns = [
    url(r'^', include('registration.backends.default.urls')),
]


if getattr(settings, 'ACCOUNT_ACTIVATION_REQUIRED', True):
    registration_view = RegistrationView
else:
    registration_view = SimpleRegistrationView

urlpatterns += [
    url(r'^register/$', registration_view.as_view(), name='registration_register'),
]
