from django import forms
from django.utils.translation import ugettext_lazy as _
from plugins.camara_deputados.models import BillInfo


class BillInfoAdminForm(forms.ModelForm):
    file_txt = forms.FileField(label=_('File in txt format'), required=False)

    class Meta:
        model = BillInfo
        fields = ('bill', 'author', 'reporting_member', 'proposal_type',
                  'proposal_number', 'proposal_year', 'situation')
