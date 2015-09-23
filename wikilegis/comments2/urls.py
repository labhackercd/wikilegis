from django.conf.urls import url, include

urlpatterns = [
    url(r'^post/$', 'wikilegis.comments2.views.post_comment', name='comments-post-comment'),
    url(r'^', include('django_comments.urls')),
]
