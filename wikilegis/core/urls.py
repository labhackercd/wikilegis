from django.conf.urls import url
from django.views.generic.base import TemplateView

urlpatterns = [
    url(r'^$', 'wikilegis.core.views.index', name='index'),
    url(r'^bill/(?P<bill_id>\d+)/$', 'wikilegis.core.views.show_bill', name='show_bill'),
    url(r'^bill/(?P<bill_id>\d+)/segments/(?P<segment_id>\d+)/$', 'wikilegis.core.views.show_segment', name='show_segment'),
    url(r'^bill/(?P<bill_id>\d+)/segments/(?P<segment_id>\d+)/amend/$', 'wikilegis.core.views.create_amendment', name='create_amendment'),
    url(r'^bill/(?P<bill_id>\d+)/segments/(?P<segment_id>\d+)/choose/(?P<amendment_id>(?:\d+|original))/$', 'wikilegis.core.views.choose_amendment', name='choose_amendment'),
    url(r'^bill/(?P<bill_id>\d+)/segments/(?P<segment_id>\d+)/unchoose/$', 'wikilegis.core.views.unchoose_amendment', name='unchoose_amendment'),
    url(r'^amendments/(?P<amendment_id>\d+)/$', 'wikilegis.core.views.show_amendment', name='show_amendment'),
    url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),
]
