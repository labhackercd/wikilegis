from django.conf.urls import url
from core import views


urlpatterns = [
    url(r'^$', views.HomeView.as_view(),
        name='home'),
    url(r'^bill/(?P<bill_id>\d+)$',
        views.HomeView.as_view(),
        name='bill_index'),
    url(r'^bill/(?P<bill_id>\d+)/amendments/(?P<segment_id>\d+)$',
        views.HomeView.as_view(),
        name='amendments_index'),
    url(r'^render/bill_info/(?P<bill_id>\d+)/$',
        views.render_bill_info, name='render_bill_info'),
    url(r'^render/bill_content/(?P<bill_id>\d+)/$',
        views.render_bill_content, name='render_bill_content'),
    url(r'^render/bill_amendments/(?P<segment_id>\d+)/$',
        views.render_bill_amendments, name='render_bill_amendments'),
    url(r'^render/amendment_comments/(?P<amendment_type>\w+)/'
        r'(?P<amendment_id>\d+)/$',
        views.render_amendment_comments, name='render_amendment_comments'),
    url(r'^render/segment_comments/(?P<segment_id>\d+)/$',
        views.render_segment_comments, name='render_segment_comments'),
    url(r'^render/new_comment/(?P<segment_id>\d+)/(?P<segment_type>\w+)/$',
        views.render_new_comment, name='render_new_segment_comments'),
    url(r'^render/vote/(?P<segment_id>\d+)/(?P<segment_type>\w+)/$',
        views.render_votes, name='render_new_vote'),
]
