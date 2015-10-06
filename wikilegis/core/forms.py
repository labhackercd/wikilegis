# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import
from operator import attrgetter
from django import forms
from django.utils.translation import ugettext_lazy as _
from wikilegis.auth2.models import User
from . import models


# TODO FIXME Meta*Form, really? C'mon, we can do better naming than this.

class GenericDataAdminForm(forms.ModelForm):

    class Meta:
        model = models.GenericData
        exclude = ('type', 'data')

    def __init__(self, *args, **kwargs):
        super(GenericDataAdminForm, self).__init__(*args, **kwargs)
        if self.instance:
            data = self.instance.data
            for k, v in data.items():
                self.initial.setdefault(k, v)

    def save(self, commit=True):
        obj = super(GenericDataAdminForm, self).save(commit=False)
        obj.type = self.get_type()
        obj.data = self.get_data()
        print(obj.data)
        if commit:
            obj.save()
        return obj

    @classmethod
    def get_type(cls):
        raise NotImplementedError

    def get_data(self):
        # All fields that are not in the original model are gonna be in the data
        opts = self._meta
        model_fields = opts.model._meta.get_fields()
        model_fields = map(attrgetter('name'), model_fields)
        return dict((field, self.cleaned_data.get(field))
                    for field in self.fields if field not in model_fields)


class MetaAuthorForm(GenericDataAdminForm):
    user = forms.ModelChoiceField(label=_('User'), queryset=User.objects.filter(is_active=True))
    title = forms.CharField(label=_('Title'), max_length=100)

    @classmethod
    def get_type(cls):
        return 'AUTHOR'

    def get_data(self):
        data = super(MetaAuthorForm, self).get_data()
        data['user'] = data['user'].pk
        return data


class MetaVideoForm(GenericDataAdminForm):
    url = forms.URLField(label=_('video url'))

    @classmethod
    def get_type(cls):
        return 'VIDEO'


class CitizenAmendmentCreationForm(forms.ModelForm):
    comment = forms.CharField(label=_("You can explain your proposal here."), widget=forms.Textarea(), required=False)

    def __init__(self, *args, **kwargs):
        super(CitizenAmendmentCreationForm, self).__init__(*args, **kwargs)
        self.fields['content'].label = _("Suggest a new proposal! You can begin editing the original one.")

    class Meta:
        model = models.CitizenAmendment
        fields = ('content',)
