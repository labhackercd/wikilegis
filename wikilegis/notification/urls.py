from django.conf.urls import url

urlpatterns = [
    url(r'^verify/(?P<bill_id>\d+)/$',
        'wikilegis.notification.views.verify_newsletter',
        name='verify_newsletter'),
]
