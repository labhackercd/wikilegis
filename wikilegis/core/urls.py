from django.conf.urls import url
from django.views.decorators.csrf import ensure_csrf_cookie
from core import views


urlpatterns = [
    url(r'^$', ensure_csrf_cookie(views.HomeView.as_view()),
        name='home'),
    url(r'^widget/(?P<pk>\d+)/?$',
        ensure_csrf_cookie(views.WidgetView.as_view()),
        name='widget_index'),
    url(r'^bill/(?P<bill_id>\d+)/?$',
        ensure_csrf_cookie(views.HomeView.as_view()),
        name='bill_index'),
    url(r'^bill/(?P<pk>\d+)/report/$', views.BillDetailView.as_view(),
        name='bill_report'),
    url(r'^bill/(?P<bill_id>\d+)/amendments/(?P<segment_id>\d+)/?$',
        ensure_csrf_cookie(views.HomeView.as_view()),
        name='amendments_index'),
    url(r'^render/bill_info/(?P<bill_id>\d+)/$',
        views.render_bill_info, name='render_bill_info'),
    url(r'^render/bill_content/(?P<bill_id>\d+)/$',
        views.render_bill_content, name='render_bill_content'),
    url(r'^render/bill_amendments/(?P<segment_id>\d+)/$',
        views.render_bill_amendments, name='render_bill_amendments'),
    url(r'^render/bill_amendment_segment/(?P<segment_id>\d+)/$',
        views.render_amendment_segment, name='render_bill_amendment_segment'),
    url(r'^render/amendment_comments/(?P<amendment_type>\w+)/'
        r'(?P<amendment_id>\d+)/$',
        views.render_amendment_comments, name='render_amendment_comments'),
    url(r'^render/segment_comments/(?P<segment_id>\d+)/$',
        views.render_segment_comments, name='render_segment_comments'),
    url(r'^render/new_comment/(?P<segment_id>\d+)/(?P<segment_type>\w+)/$',
        views.render_new_comment, name='render_new_segment_comments'),
    url(r'^render/vote/(?P<segment_id>\d+)/(?P<segment_type>\w+)/$',
        views.render_votes, name='render_new_vote'),
    url(r'^render/new_amendment/(?P<segment_id>\d+)/(?P<amendment_type>\w+)/$',
        views.render_new_amendment, name='render_new_amendment'),
]
