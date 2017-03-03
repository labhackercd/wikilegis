from django.conf.urls import url
from notification import views

urlpatterns = [
    url(r'^subscribe/(?P<bill_id>\d+)/$',
        views.render_newsletter_info,
        name='subscribe_newsletter'),
]
