
from django.http import HttpResponseForbidden, HttpResponseRedirect, Http404
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.conf import settings
from django_comments.models import Comment
from django.utils.translation import ugettext, ugettext_lazy as _
from distutils.util import strtobool
from django.views.generic import FormView, RedirectView, DetailView
from django.views.decorators.clickjacking import xframe_options_exempt

from wikilegis.core.models import Bill, BillSegment, UpDownVote
from wikilegis.core.decorators import open_for_partifipations


class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'widget/login.html'

    @xframe_options_exempt
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        next_url = self.request.POST.get('next', None)
        if next_url:
            return next_url
        else:
            raise Http404()


class LogoutView(RedirectView):

    @xframe_options_exempt
    def dispatch(self, *args, **kwargs):
        return super(LogoutView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        next_url = self.request.GET.get('next', None)
        if next_url:
            return next_url
        else:
            raise Http404()


class WidgetView(DetailView):
    model = Bill
    template_name = "widget/widget.html"

    @xframe_options_exempt
    def dispatch(self, *args, **kwargs):
        return super(WidgetView, self).dispatch(*args, **kwargs)

    def get_object(self, queryset=None):
        obj = super(WidgetView, self).get_object(queryset)
        if obj.status == 'draft':
            raise Http404
        return obj


@xframe_options_exempt
@open_for_partifipations
def amendment(request, segment_id):
    if request.user.is_authenticated():
        replaced = BillSegment.objects.get(pk=segment_id)
        segment = BillSegment()
        segment.replaced = replaced
        segment.bill = replaced.bill
        segment.author = request.user
        segment.original = False
        segment.content = request.POST.get('amendment')
        segment.type = replaced.type
        segment.number = replaced.number
        segment.order = replaced.order
        segment.save()
        html = render_to_string('widget/_amendments.html',
                                {'segment': replaced, 'user': request.user})
        return JsonResponse({'html': html,
                             'count': replaced.substitutes.all().count()})
    else:
        msg = _("You must be logged to suggest a new amendment.")
        return HttpResponseForbidden(reason=msg)


@xframe_options_exempt
@open_for_partifipations
def updown_vote(request, segment_id):
    if request.user.is_authenticated():
        segment = BillSegment.objects.get(pk=segment_id)

        ctype = ContentType.objects.get_for_model(BillSegment)
        vote = UpDownVote.objects.get_or_create(
            object_id=segment_id,
            content_type=ctype,
            user=request.user
        )[0]
        if request.method == 'POST':
            vote.vote = strtobool(request.POST['vote'])
            vote.save()
        elif request.method == 'DELETE':
            vote.delete()
        elif request.method == 'PUT':
            return HttpResponseForbidden()
        html = render_to_string('widget/_action_votes.html',
                                {'segment': segment, 'user': request.user})
        return JsonResponse({'html': html})
    else:
        msg = _("You must be logged to vote.")
        return HttpResponseForbidden(reason=msg)


@xframe_options_exempt
@open_for_partifipations
def comment(request, segment_id):
    if request.user.is_authenticated() and request.method == 'POST':
        ctype = ContentType.objects.get_for_model(BillSegment)
        segment = BillSegment.objects.get(pk=segment_id)
        obj = Comment()
        obj.content_type = ctype
        obj.user = request.user
        obj.comment = request.POST.get('comment')
        obj.object_pk = segment_id
        obj.site_id = settings.SITE_ID
        obj.save()
        html = render_to_string('widget/_segment_comments.html',
                                {'segment': segment})
        return JsonResponse({'html': html,
                             'count': segment.comments.all().count()})
    else:
        msg = _("You must be logged to comment.")
        return HttpResponseForbidden(reason=msg)
