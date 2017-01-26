from django.conf.urls import url
from django.views.generic.base import TemplateView
from core import views


urlpatterns = [
    url(r'^', TemplateView.as_view(template_name='home.html'),
        name='home'),
    url(r'^render/bill_info/(?P<bill_id>\d+)/$', views.render_bill_info,
        name='render_bill_info'),
    url(r'^render/bill_content/(?P<bill_id>\d+)/$', views.render_bill_content,
        name='render_bill_content'),
    url(r'^render/bill_interactions/(?P<segment_id>\d+)/$', views.render_bill_interactions,
        name='render_bill_interactions'),
]
