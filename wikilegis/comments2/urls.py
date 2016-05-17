from django.conf.urls import include
from django.conf.urls import url

urlpatterns = [
    url(r'^post/$', 'wikilegis.comments2.views.post_comment', name='comments-post-comment'),
    url(r'^', include('django_comments.urls')),
]
