# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import
from datetime import datetime
from django.core.exceptions import ValidationError
from django import forms
from django.utils.translation import ugettext_lazy as _
from . import models
from operator import attrgetter
import requests
from wikilegis.auth2.models import User
from xml.etree import ElementTree


# TODO(NAME) FIXME Meta*Form, really? C'mon, we can do better naming than this.
# from wikilegis.core.views import add_proposition
from wikilegis.core.models import Bill
from wikilegis.core.models import BillSegment
from wikilegis.core.models import Proposition
from wikilegis.core.models import TypeSegment


class GenericDataAdminForm(forms.ModelForm):

    class Meta(object):
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
    comment = forms.CharField(
        label=_("You can explain your proposal here."),
        widget=forms.Textarea(), required=False)

    def __init__(self, *args, **kwargs):
        super(CitizenAmendmentCreationForm, self).__init__(*args, **kwargs)
        self.fields['content'].label = _(
            "Suggest a new proposal! You can begin editing the original one.")

    class Meta(object):
        model = models.BillSegment
        fields = ('content',)


class BillAdminForm(forms.ModelForm):
    PROPOSITION_TYPE_CHOICES = (
        ('', _('Select a type')),
        ('PEC', 'PEC - Proposta de Emenda à Constituição'),
        ('PLP', 'PLP - Projeto de Lei Complementar'),
        ('PL', 'PL - Projeto de Lei'),
        ('MPV', 'MPV - Medida Provisória')
    )
    type = forms.ChoiceField(label=_('Type'), choices=PROPOSITION_TYPE_CHOICES, required=False)
    number = forms.IntegerField(label=_('Number'), required=False)
    year = forms.IntegerField(label=_('Year'), required=False)

    def __init__(self, *args, **kwargs):
        super(BillAdminForm, self).__init__(*args, **kwargs)
        try:
            proposition = kwargs['instance'].proposition_set.all()[0]
            self.fields['type'].initial = proposition.type.strip()
            self.fields['number'].initial = proposition.number
            self.fields['year'].initial = proposition.year
        except Exception:
            pass

    class Meta(object):
        model = models.Bill
        fields = ('title', 'description', 'status', 'editors', 'type', 'number', 'year')

    def clean(self):
        if self.data['type'] or self.data['number'] or self.data['year']:
            if not self.data['type'] or not self.data['number'] or not self.data['year']:
                msg = ""
                self.add_error('type', msg)
                self.add_error('number', msg)
                self.add_error('year', msg)
                raise ValidationError(_('When adding a field in the legislative proposal, '
                                        'the three fields are now required'))
        return self.cleaned_data

    def save(self, commit=True):
        instance = super(BillAdminForm, self).save(commit=False)
        instance.save()
        self.save_m2m()
        if self.cleaned_data['type'] and self.cleaned_data['number'] and self.cleaned_data['year']:
            if instance.proposition_set.all():
                delete_proposition(instance.proposition_set.all()[0].id_proposition)
            try:
                params = {
                    'tipo':
                    self.cleaned_data['type'],
                    'numero': self.cleaned_data['number'],
                    'ano': self.cleaned_data['year']}
                response = requests.get(
                    'http://www.camara.gov.br/SitCamaraWS/Proposicoes.asmx/ObterProposicao',
                    params=params)
                create_proposition(response, instance.id)
            except Exception:
                pass
        else:
            try:
                delete_proposition(instance.proposition_set.all()[0].id_proposition)
            except Exception:
                pass
        return instance


def delete_proposition(proposition_id):
    proposition = Proposition.objects.get(id_proposition=proposition_id)
    proposition.delete()


def create_proposition(response, bill_id):
    tree = ElementTree.fromstring(response.content)
    proposition = Proposition()
    proposition.bill_id = bill_id
    proposition.type = tree.attrib['tipo']
    proposition.number = tree.attrib['numero']
    proposition.year = tree.attrib['ano']
    proposition.name_proposition = tree.find('nomeProposicao').text
    if tree.find('idProposicao').text.isdigit():
        proposition.id_proposition = int(tree.find('idProposicao').text)
    if tree.find('idProposicaoPrincipal').text.isdigit():
        proposition.id_main_proposition = int(tree.find('idProposicaoPrincipal').text)
    proposition.name_origin_proposition = tree.find('idProposicaoPrincipal').text
    proposition.theme = tree.find('tema').text
    proposition.menu = tree.find('Ementa').text
    proposition.menu_explanation = tree.find('ExplicacaoEmenta').text
    proposition.author = tree.find('Autor').text
    proposition.id_register = tree.find('ideCadastro').text
    proposition.uf_author = tree.find('ufAutor').text
    proposition.party_author = tree.find('partidoAutor').text
    proposition.apresentation_date = datetime.strptime(
        tree.find('DataApresentacao').text, '%d/%m/%Y').date()
    proposition.processing_regime = tree.find('RegimeTramitacao').text
    proposition.last_dispatch_date = datetime.strptime(
        tree.find('UltimoDespacho').attrib['Data'], '%d/%m/%Y').date()
    proposition.last_dispatch = tree.find('UltimoDespacho').text
    proposition.appraisal = tree.find('Apreciacao').text
    proposition.indexing = tree.find('Indexacao').text
    proposition.situation = tree.find('Situacao').text
    proposition.content_link = tree.find('LinkInteiroTeor').text

    proposition.save()


def update_proposition(response, proposition_id):
    tree = ElementTree.fromstring(response.content)
    proposition = Proposition.objects.get(id_proposition=proposition_id)
    proposition.type = tree.attrib['tipo']
    proposition.number = tree.attrib['numero']
    proposition.year = tree.attrib['ano']
    proposition.name_proposition = tree.find('nomeProposicao').text
    if tree.find('idProposicao').text.isdigit():
        proposition.id_proposition = int(tree.find('idProposicao').text)
    if tree.find('idProposicaoPrincipal').text.isdigit():
        proposition.id_main_proposition = int(tree.find('idProposicaoPrincipal').text)
    proposition.name_origin_proposition = tree.find('idProposicaoPrincipal').text
    proposition.theme = tree.find('tema').text
    proposition.menu = tree.find('Ementa').text
    proposition.menu_explanation = tree.find('ExplicacaoEmenta').text
    proposition.author = tree.find('Autor').text
    proposition.id_register = tree.find('ideCadastro').text
    proposition.uf_author = tree.find('ufAutor').text
    proposition.party_author = tree.find('partidoAutor').text
    proposition.apresentation_date = datetime.strptime(
        tree.find('DataApresentacao').text, '%d/%m/%Y').date()
    proposition.processing_regime = tree.find('RegimeTramitacao').text
    proposition.last_dispatch_date = datetime.strptime(
        tree.find('UltimoDespacho').attrib['Data'], '%d/%m/%Y').date()
    proposition.last_dispatch = tree.find('UltimoDespacho').text
    proposition.appraisal = tree.find('Apreciacao').text
    proposition.indexing = tree.find('Indexacao').text
    proposition.situation = tree.find('Situacao').text
    proposition.content_link = tree.find('LinkInteiroTeor').text

    proposition.save()


class AddProposalForm(forms.ModelForm):
    comment = forms.CharField(
        label=_("You can explain your proposal here."),
        widget=forms.Textarea(),
        required=False)

    def __init__(self, *args, **kwargs):
        self.bill_id = kwargs.pop('bill_id')
        super(AddProposalForm, self).__init__(*args, **kwargs)
        self.fields['type'].queryset = TypeSegment.objects.filter(editable=True)
        self.fields['parent'].queryset = BillSegment.objects.filter(
            bill__id=self.bill_id, original=True)

    class Meta(object):
        model = BillSegment
        fields = ('parent', 'type', 'content')


class BillSegmentAdminForm(forms.ModelForm):
    try:
        bill = forms.ModelChoiceField(label=_('bill'),
                                      queryset=Bill.objects.all(),
                                      initial=Bill.objects.latest('id').id)
        parent = forms.ModelChoiceField(label=_('segment parent'),
                                        queryset=BillSegment.objects.filter(
                                            bill_id=Bill.objects.latest('id').id,
                                            original=True).order_by('-id'),
                                        required=False)
    except Exception:
        bill = forms.ModelChoiceField(label=_('bill'), queryset=Bill.objects.all())

    class Meta(object):
        model = BillSegment
        fields = ('bill', 'order', 'parent', 'type', 'number', 'content')
