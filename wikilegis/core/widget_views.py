
from django.http import HttpResponseForbidden, HttpResponseRedirect, Http404
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.conf import settings
from django_comments.models import Comment
from distutils.util import strtobool
from django.views.generic import FormView, RedirectView, DetailView

from wikilegis.core.models import Bill, BillSegment, UpDownVote


class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'widget/login.html'

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

    def get_object(self, queryset=None):
        obj = super(WidgetView, self).get_object(queryset)
        if obj.status == 'draft':
            raise Http404
        return obj


def amendment(request, segment_id):
    if request.user.is_authenticated():
        replaced = BillSegment.objects.get(pk=segment_id)
        if replaced.bill.status == 'closed':
            return HttpResponseForbidden(reason='Projeto encerrado')
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
        return HttpResponseForbidden(reason='Loga ai cara')


def updown_vote(request, segment_id):
    if request.user.is_authenticated():
        segment = BillSegment.objects.get(pk=segment_id)
        if segment.bill.status == 'closed':
            return HttpResponseForbidden(reason='Projeto encerrado')

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
        return HttpResponseForbidden(reason='Loga ai cara')


def comment(request, segment_id):
    if request.user.is_authenticated() and request.method == 'POST':
        ctype = ContentType.objects.get_for_model(BillSegment)
        segment = BillSegment.objects.get(pk=segment_id)
        if segment.bill.status == 'closed':
            return HttpResponseForbidden(reason='Projeto encerrado')
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
        return HttpResponseForbidden(reason='Loga ai cara')
