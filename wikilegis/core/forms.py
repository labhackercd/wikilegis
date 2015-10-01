# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import
from django import forms
from . import models


class CitizenAmendmentCreationForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(), required=False)

    class Meta:
        model = models.CitizenAmendment
        fields = ('content',)
