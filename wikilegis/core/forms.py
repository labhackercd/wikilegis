# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import
from django import forms
from django.utils.translation import ugettext_lazy as _
from wikilegis.auth2.models import User
from . import models


class MetaAuthorForm(forms.ModelForm):
    user = forms.ModelChoiceField(label=_('User'), queryset=User.objects.filter(is_active=True))
    title = forms.CharField(label=_('Title'), max_length=100)

    class Meta:
        model = models.GenericData
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(MetaAuthorForm, self).__init__(*args, **kwargs)
        if self.instance:
            data = self.instance.data
            for k, v in data.items():
                self.initial.setdefault(k, v)

    def save(self, commit=True):
        obj = super(MetaAuthorForm, self).save(commit=False)
        obj.type = 'AUTHOR'
        user = self.cleaned_data['user'].pk
        title = self.cleaned_data['title']
        obj.data = dict(user=user, title=title)
        if commit:
            obj.save()
        return obj


class CitizenAmendmentCreationForm(forms.ModelForm):
    comment = forms.CharField(label=_("Comment about your proposal."), widget=forms.Textarea(), required=False)
    
    def __init__(self, *args, **kwargs):
      super(CitizenAmendmentCreationForm, self).__init__(*args, **kwargs)
      self.fields['content'].label = _("Suggest a new proposal! You can begin editing the original one.")

    class Meta:
        model = models.CitizenAmendment
        fields = ('content',)
