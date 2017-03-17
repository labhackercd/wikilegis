from django.conf.urls import url, include
from django.views.generic.edit import CreateView
from accounts.forms import UserCreationForm
from accounts.views import WidgetLoginView

urlpatterns = [
    url('^accounts/register/', CreateView.as_view(
        template_name='registration/register.html',
        form_class=UserCreationForm,
        success_url='/')),
    url('^accounts/', include('django.contrib.auth.urls')),
    url(r'^widget/login/$', WidgetLoginView.as_view(), name='widget_login'),
    url(r'^widget/signup/$', CreateView.as_view(
        template_name='registration/register.html',
        form_class=UserCreationForm,
        success_url='widget_login'), name='widget_signup'),
]
