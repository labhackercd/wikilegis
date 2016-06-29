# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import ugettext
from django.views.generic import RedirectView
from registration.models import RegistrationProfile

from wikilegis.auth2.forms import UserProfileEditionForm
from wikilegis.auth2.models import User


def resend_activation(request):
    if request.method == 'POST':
        user = RegistrationProfile.objects.get(user__email=request.POST['email'])
        user.send_activation_email(Site.objects.get_current(), request)
        return redirect("registration_complete")

    return render(request, 'registration/resend_activation_form.html')


class ActivationCompleteView(RedirectView):
    pattern_name = 'index'

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('permanent', False)
        super(ActivationCompleteView, self).__init__(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        messages.info(request, ugettext("Your account is now activated."))
        return super(ActivationCompleteView, self).get(request, *args, **kwargs)


@login_required
def your_profile(request):
    if request.method == 'POST':
        form = UserProfileEditionForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, ugettext('Profile successfully updated'))
            return redirect("edit_profile")
    else:
        form = UserProfileEditionForm(instance=request.user)

    return render(request, 'auth2/your_profile.html', {'form': form})


@login_required
def show_users_profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'auth2/show_users_profile.html', {'user': user})
