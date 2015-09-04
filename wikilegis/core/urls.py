from django.conf.urls import url

urlpatterns = [
    url(r'^$', 'wikilegis.core.views.index', name='index'),
    url(r'^bill/(?P<bill_id>\d+)/$', 'wikilegis.core.views.show_bill', name='show_bill'),
    url(r'^bill/(?P<bill_id>\d+)/segments/(?P<segment_id>\d+)/$', 'wikilegis.core.views.show_segment', name='show_segment'),
    url(r'^bill/(?P<bill_id>\d+)/segments/(?P<segment_id>\d+)/amend/$', 'wikilegis.core.views.create_amendment', name='create_amendment'),
]
