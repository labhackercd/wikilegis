from django.conf.urls import url
from django.views.generic.base import TemplateView

from wikilegis.core.api import (BillListAPI, SegmentsListAPI, CommentListAPI,
                                api_root, UserUpdateAPI, UserAPI, BillAPI,
                                TypeSegmentAPI, UpDownVoteListAPI,
                                CreateUserAPI, VoteUpdateDeleteAPI)
from wikilegis.core.views import BillReport, CreateProposal, BillDetailView

urlpatterns = [
    url(r'^$', 'wikilegis.core.views.index', name='index'),
    url(r'^bill/(?P<pk>\d+)/$', BillDetailView.as_view(),
        name='show_bill'),
    url(r'^bill/(?P<bill_id>\d+)/proposal/$', CreateProposal.as_view(),
        name='create_proposal'),
    url(r'^bill/(?P<bill_id>\d+)/proposal/(?P<segment_id>\d+)/$',
        'wikilegis.core.views.show_proposal', name='show_proposal'),
    url(r'^bill/(?P<bill_id>\d+)/segments/(?P<segment_id>\d+)/$',
        'wikilegis.core.views.show_segment', name='show_segment'),
    url(r'^bill/(?P<bill_id>\d+)/segments/(?P<segment_id>\d+)/amend/$',
        'wikilegis.core.views.create_amendment', name='create_amendment'),
    url(r'^amendments/(?P<amendment_id>\d+)/$',
        'wikilegis.core.views.show_amendment', name='show_amendment'),
    url(r'^about/$', TemplateView.as_view(template_name='about.html'),
        name='about'),
    url(r'^bill/(?P<pk>\d+)/report/$', BillReport.as_view(),
        name='bill_report'),
    url(r'^upvote/(?P<content_type>\d+)/(?P<object_id>\d+)/$',
        'wikilegis.core.views.upvote', name='upvote'),
    url(r'^downvote/(?P<content_type>\d+)/(?P<object_id>\d+)/$',
        'wikilegis.core.views.downvote', name='downvote'),
]

urlpatterns += [
    url(r'^api/$', api_root),
    url(r'^api/bills/$', BillListAPI.as_view(),
        name='bill_list_api'),
    url(r'^api/bills/(?P<pk>\d+)$', BillAPI.as_view(),
        name='bill_api'),
    url(r'^api/segment_types/$', TypeSegmentAPI.as_view(),
        name='types_segments_list_api'),
    url(r'^api/segments/$', SegmentsListAPI.as_view(),
        name='segments_list_api'),
    url(r'^api/comments/$', CommentListAPI.as_view(),
        name='comment_list_api'),
    url(r'^api/user/update/$', UserUpdateAPI.as_view(),
        name='user_update_api'),
    url(r'^api/user/create/$', CreateUserAPI.as_view(),
        name='user_create_api'),
    url(r'^api/users/$', UserAPI.as_view(),
        name='users_list_api'),
    url(r'^api/votes/$', UpDownVoteListAPI.as_view(),
        name='votes_api'),
    url(r'^api/votes/update/(?P<pk>\d+)$', VoteUpdateDeleteAPI.as_view(),
        name='votes_update_api'),
]
