from django.conf.urls import url

urlpatterns = [
    url(r'^signup/$', 'wikilegis.auth2.views.signup', name='signup'),
]
