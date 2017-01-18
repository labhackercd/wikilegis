from django.conf.urls import url
from django.views.generic.base import TemplateView
from registration.backends.default.views import RegistrationView
from wikilegis.core.api import (BillListAPI, SegmentsListAPI, CommentListAPI,
                                api_root, UserUpdateAPI, UserAPI, BillAPI,
                                TypeSegmentAPI, UpDownVoteListAPI,
                                CreateUserAPI, VoteUpdateDeleteAPI,
                                NewsleterListAPI)
from wikilegis.core import views
from wikilegis.core import widget_views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^bill/(?P<pk>\d+)/$', views.BillDetailView.as_view(),
        name='show_bill'),
    url(r'^bill/(?P<pk>\d+)/references/$',
        views.BillDetailView.as_view(template_name='bill/references.html'),
        name='bill_references'),
    url(r'^bill/(?P<bill_id>\d+)/proposal/$', views.CreateProposal.as_view(),
        name='create_proposal'),
    url(r'^bill/(?P<bill_id>\d+)/proposal/(?P<segment_id>\d+)/$',
        views.show_proposal, name='show_proposal'),
    url(r'^bill/(?P<bill_id>\d+)/segments/(?P<segment_id>\d+)/$',
        views.show_segment, name='show_segment'),
    url(r'^bill/(?P<bill_id>\d+)/segments/(?P<segment_id>\d+)/amend/$',
        views.create_amendment, name='create_amendment'),
    url(r'^amendments/(?P<amendment_id>\d+)/$',
        views.show_amendment, name='show_amendment'),
    url(r'^about/$', TemplateView.as_view(template_name='about.html'),
        name='about'),
    url(r'^bill/(?P<pk>\d+)/report/$', views.BillReport.as_view(),
        name='bill_report'),
    url(r'^upvote/(?P<content_type>\d+)/(?P<object_id>\d+)/$',
        views.upvote, name='upvote'),
    url(r'^downvote/(?P<content_type>\d+)/(?P<object_id>\d+)/$',
        views.downvote, name='downvote'),
]

urlpatterns += [
    url(r'^widget/(?P<pk>\d+)/?$', widget_views.WidgetView.as_view(),
        name='widget'),
    url(r'^widget/login/$', widget_views.LoginView.as_view(),
        name='widget_login'),
    url(r'^widget/signup/$', RegistrationView.as_view(
        success_url='widget_login',
        template_name='widget/login.html'), name='widget_signup'),
    url(r'^widget/vote/(?P<segment_id>\d+)$', widget_views.updown_vote,
        name='widget_vote'),
    url(r'^widget/amendment/(?P<segment_id>\d+)$', widget_views.amendment,
        name='widget_amendment'),
    url(r'^widget/comment/(?P<segment_id>\d+)$', widget_views.comment,
        name='widget_comment'),
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
    url(r'^api/newsletter/$', NewsleterListAPI.as_view(),
        name='newsletter_api'),
]
