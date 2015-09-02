from django.conf.urls import url

urlpatterns = [
    url(r'^$', 'wikilegis.core.views.index'),
    url(r'^bill/(?P<bill_id>\d+)/$', 'wikilegis.core.views.show_bill', name='show_bill')
]
