from django.conf.urls import url

urlpatterns = [
    url(r'^$', 'wikilegis.core.views.index', name='index'),
    url(r'^bill/(?P<bill_id>\d+)/$', 'wikilegis.core.views.show_bill', name='show_bill'),
    url(r'^bill/(?P<bill_id>\d+)/segments/(?P<segment_id>\d+)/$', 'wikilegis.core.views.show_segment', name='show_segment'),
]
