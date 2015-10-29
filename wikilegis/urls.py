from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
import object_tools

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('wikilegis.auth2.urls')),
    url(r'^accounts/social/', include('social.apps.django_app.urls', namespace=settings.SOCIAL_AUTH_URL_NAMESPACE)),
    url(r'^comments/', include('wikilegis.comments2.urls')),
    url(r'^search/', include('haystack.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^', include('wikilegis.core.urls')),
    url(r'^object-tools/', include('object_tools.tests.urls')),
]

admin.site.site_header = 'Wikilegis'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
