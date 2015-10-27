# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.utils.translation import ugettext
from django.views.generic import RedirectView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .forms import UserForm
from wikilegis.auth2.models import User


class ActivationCompleteView(RedirectView):
    pattern_name = 'index'

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('permanent', False)
        super(ActivationCompleteView, self).__init__(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        messages.info(request, ugettext("Your account is now activated."))
        return super(ActivationCompleteView, self).get(request, *args, **kwargs)


@login_required
def edit_profile(request):
    user = User.objects.get(pk=request.user.pk)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return render(request, 'registration/edit.html/', {'form': form})
        else:
            return HttpResponse("This is not working...")
    else:
        form = UserForm(instance=user)
        return render(request, 'registration/edit.html/', {'form': form})
