from django.conf.urls import url, include
from wikilegis.comments2 import views

urlpatterns = [
    url(r'^post/$', views.post_comment, name='comments-post-comment'),
    url(r'^', include('django_comments.urls')),
]
