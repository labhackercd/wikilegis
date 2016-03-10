from django.conf.urls import url

urlpatterns = [
    url(r'^verify/(?P<bill_id>\d+)/(?P<periodicity>[\w_-]+)/$',
        'wikilegis.notification.views.verify_newsletter', name='verify_newsletter'),
]
