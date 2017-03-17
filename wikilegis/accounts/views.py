from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.generic import FormView


class WidgetLoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'widget/login.html'

    @xframe_options_exempt
    def dispatch(self, *args, **kwargs):
        return super(WidgetLoginView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        next_url = self.request.POST.get('next', None)
        if next_url:
            return next_url
        else:
            raise Http404()
