from django.conf.urls import url, include
from django.views.generic.edit import CreateView
from accounts.forms import UserCreationForm

urlpatterns = [
    url('^accounts/register/', CreateView.as_view(
        template_name='registration/register.html',
        form_class=UserCreationForm,
        success_url='/')),
    url('^accounts/', include('django.contrib.auth.urls')),
]
