from django.conf import settings
from django.utils import translation


class ForceLangMiddleware:

    def process_request(self, request):
        request.LANG = getattr(settings, 'LANGUAGE_CODE', settings.LANGUAGE_CODE)
        translation.activate(request.LANG)
        request.LANGUAGE_CODE = request.LANG
