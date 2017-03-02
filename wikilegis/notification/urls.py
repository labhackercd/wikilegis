from django.conf.urls import url
from notification import views

urlpatterns = [
    url(r'^verify/(?P<bill_id>\d+)/$',
        views.verify_newsletter,
        name='verify_newsletter'),
]
