# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.utils.translation import ugettext
from django.views.generic import RedirectView


class ActivationCompleteView(RedirectView):
    pattern_name = 'index'

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('permanent', False)
        super(ActivationCompleteView, self).__init__(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        messages.info(request, ugettext("Your account is now activated."))
        return super(ActivationCompleteView, self).get(request, *args, **kwargs)
