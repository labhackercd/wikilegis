# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.translation import ugettext
from django.views.generic import RedirectView

from .forms import UserForm


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
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, ugettext('Profile successfully updated'))
            return redirect("edit_profile")
    else:
        form = UserForm(instance=request.user)

    return render(request, 'registration/edit.html/', {'form': form})
